from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
app = Flask(__name__)



@app.route('/')
def start():
    return render_template("home.html")

@app.route("/question/<int:page>")
def question(page):
    print("pageNo", page)
    with open("toon_score.json", "r", encoding="utf-8") as f:
       dict = json.load(f)
       print(dict)
       for i in range(len(dict)):
           
           print(dict[i]["now"])
    return render_template("question.html")


if __name__ == '__main__':
    app.run(debug=True)
