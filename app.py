from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
import subprocess
import random
import json
from config import config
from importSQL import db
from models import User, Submission, UserSession, Code

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

db.init_app(app)


# test_case.json 파일을 읽어 problems 변수에 저장
with open('test_case.json', encoding='utf-8') as f:
    raw_data = json.load(f)

with open('problem_hard.json', encoding='utf-8') as f:
    problem_levels = json.load(f)

# JSON 형식에 맞게 problems 변환
problems = {}
for pid_str, pdata in raw_data['problems'].items():
    pid = int(pid_str)
    inputs = []
    outputs = []
    for case in pdata['test_cases']:
        inputs.append(str(case['input']))
        outputs.append(str(case['output']).strip())
    problems[pid] = {
        'title': pdata['title'],
        'description': pdata['description'],
        'input': inputs,
        'output': outputs
    }

@app.route('/')
def home():
    todays_problem = random.choice(list(problems.keys()))
    
    # 난이도별 문제 리스트
    # 각 단계에 문제의 ID와 제목을 가져오기
    level_data = []
    for level in problem_levels:
        level_name = level['step']
        problem_list = []
        for pid in level['problems']:
            if pid in problems:
                problem_list.append({
                    'id': pid,
                    'title': problems[pid]['title']
                })
        level_data.append({
            'level_name': level_name,
            'problems': problem_list
        })
    
    return render_template('home.html', 
                           todays_problem=todays_problem, 
                           level_data=level_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        checkpassword = request.form['checkpassword']
        password = request.form['password']
        username = request.form['username']
        usernickname = request.form['usernickname']
    
        if len(username) < 4:
            return render_template('signup.html', message="아이디를 4자 이상 입력해주세요")

        if checkpassword != password or not (8 <= len(password) < 16):
            return render_template('signup.html', message="비밀번호를 다시 확인해주세요.")

        if password.islower():
            return render_template('signup.html', message="대소문자 포함 여부를 확인해주세요.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', message="이미 존재하는 사용자명입니다.")

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, nickname=usernickname)
            db.session.add(new_user)
            db.session.commit()

            flash(usernickname + "님 회원가입이 완료되었습니다! 로그인해주세요.")
            return redirect('/login')
        
        except SQLAlchemyError:
            db.session.rollback()
            return render_template('signup.html', message="회원가입 중 오류가 발생했습니다.")

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['nickname'] = user.nickname
            session['logged_in'] = True
            
            flash(f"{user.nickname}님 환영합니다!")
            return redirect('/')
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
    
    return render_template('login.html')

@app.route("/search", methods=["GET"])
def search_problem():
    query = request.args.get("query", "").strip().lower()

    if query.isdigit():
        pid = int(query)
        if pid in problems:
            return redirect(url_for("problem", pid=pid))

    for pid, pdata in problems.items():
        if query in pdata['title'].lower():
            return redirect(url_for("problem", pid=pid))

    flash("검색 결과가 없습니다.")
    return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.clear()
    flash("로그아웃되었습니다.")
    return redirect('/')

@app.route('/allproblem')
def allproblem():
    best_scores = {}

    if 'user_id' in session:
        user_id = session['user_id']

        # 사용자의 모든 제출 기록 조회
        submissions = Submission.query.filter_by(user_id=user_id).all()

        # 문제별 최고 점수 계산
        for sub in submissions:
            pid = sub.problem_id  # 이미 int로 저장되어 있을 수 있음
            if pid not in best_scores or sub.score > best_scores[pid]:
                best_scores[pid] = sub.score

    return render_template('allproblem.html', problems=problems, best_scores=best_scores)

@app.route('/solvedproblem')
def solvedproblem():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    with app.app_context():
        submissions = Submission.query.filter_by(user_id=session['user_id']).order_by(Submission.submitted_at.desc()).all()

    return render_template("solvedproblem.html", submissions=submissions)

@app.route('/problem/<int:pid>', methods=['GET', 'POST'])
def problem(pid):
    problem = problems.get(pid)
    if not problem:
        return "문제를 찾을 수 없습니다.", 404

    logged_in = session.get('logged_in', False)
    results = []
    score = None

    if request.method == 'POST':
        usercode = request.form['usercode']

        if not logged_in:
            # 로그인 안 된 상태면 제출 처리 안 하고 템플릿에 로그인 상태 전달
            return render_template("problem_template.html", problem=problem, pid=pid, results=[], logged_in=logged_in)

        with open('user_solution.py', 'w', encoding='utf-8') as f:
            f.write(usercode)

        for i, input_data in enumerate(problem['input']):
            proc = subprocess.Popen(
                ['python', 'user_solution.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                stdout, stderr = proc.communicate(input=input_data, timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                results.append({'input': input_data, 'result': 'Timeout'})
                continue

            output = stdout.strip()
            print(output)
            correct = (output == problem['output'][i])
            results.append({
                'input': input_data,
                'expected': problem['output'][i],
                'output': output,
                'correct': correct,
                'error': stderr.strip()
            })
        
        correct_count = sum(1 for value in results if value.get('correct'))
        total_count = len(results)
        score = int((correct_count/total_count)*100) if total_count > 0 else 0
    
        # 결과를 DB에 저장 (models.py 내 Submission 모델 필요)
        submission = Submission(
            user_id=session['user_id'],
            problem_id=pid,
            code=usercode,
            result=results,
            score=score
        )
        db.session.add(submission)
        db.session.commit()

    return render_template("problem_template.html", problem=problem, pid=pid, results=results, logged_in=logged_in, score=score)

if __name__ == '__main__':
    print("\nFlask 서버 시작...")
    app.run(debug=True)