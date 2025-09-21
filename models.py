from datetime import datetime
from importSQL import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 정의
    submissions = db.relationship('Submission', backref='user', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('UserSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

    
    @staticmethod
    def create_user(username, password, nickname):
        """새 사용자 생성"""
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, nickname=nickname)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_username(username):
        """사용자명으로 사용자 조회"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def authenticate(username, password):
        """사용자 인증"""
        from werkzeug.security import check_password_hash
        user = User.get_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Text, nullable=False)
    result = db.Column(db.JSON, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'
    
    def all_correct(self):
        """제출 결과가 모두 맞으면 True 반환"""
        try:
            if isinstance(self.result, str):
                import json
                result_data = json.loads(self.result)
            else:
                result_data = self.result
            
            return all(r.get('correct', False) for r in result_data)
        except Exception as e:
            print(f"Error in all_correct: {e}")
            return False

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<UserSession {self.session_token}>' 
    
class Code(db.Model):
    __tablename__ = "code"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 기본키
    user = db.Column(db.String(120), nullable=False)  # 유저 이메일
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 제출 시간
    success = db.Column(db.Boolean, default=False)  # 성공 여부

    def __repr__(self):
        return f"<Code {self.id}, user={self.user}, success={self.success}>"