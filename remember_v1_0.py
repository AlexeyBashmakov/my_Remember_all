from flask import Flask, render_template, request
import json
import os

class Remember:
    # словарь json вопросов
    dictJ = {}
    current_course = ""
    current_question = 1
    last_key = 1
    mode = ""
    
    def __init__(self):
        with open("data.json", "r") as f:
            self.dictJ = json.load(f)
        self.courses = len(self.dictJ)
        if os.path.exists("templates/remember.html"):
            os.remove("templates/remember.html")
        

app = Flask(__name__)
A = Remember()

def generate_remember():
    page = """{% extends "base.html" %}

{% block body %}

<form method="POST" action="/question">
<table>\n"""
    for course, questions in A.dictJ.items():
        page += f"  <tr><td class='name_questions'>{course}</td><td class='name_questions counts_questions'>{len(questions)}</td><td><input class='btn' name='{course}' type='SUBMIT' value='По порядку'></td><td><input class='btn' name='{course}' type='SUBMIT' value='Случайно'></td></tr>\n"
    page += """</table>\n
</form>

{% endblock %}"""
    with open("templates/remember.html", "w", encoding = "utf-8") as f:
        f.write(page)

@app.route("/")
def hello() -> str:
    return "Hello from Flask!"
    
@app.route("/remember")
def remember():
    generate_remember()
    A.current_question = 1
    return render_template("remember.html", the_title = "Вспомнить всё")

@app.route("/question", methods=["GET", "POST"])
def question():
    res = {}
    if len(request.form) != 0:
    # k - имя нажатой кнопки
    # v - надпись на ней
        for k, v in request.form.items():
            res[k] = v
    
        question_str = ""
        k = list(res)[0]
        v = res[k]
        if k == "next":
            if (A.current_question + 1) > A.last_key:
                A.current_question = 1
            else:
                A.current_question += 1
            question_str = A.dictJ[A.current_course][str(A.current_question)]
        else:
            A.current_course = k
            A.last_key = max([int(x) for x in A.dictJ[A.current_course].keys()])
            if res[A.current_course] == "По порядку":
                A.mode = "По порядку"
                question_str = A.dictJ[A.current_course][str(A.current_question)]
            elif res[A.current_course] == "Случайно":
                A.mode = "Случайно"
                question_str = "Режим случайного перебора вопросов ещё не готов!"
            else:
                question_str = "Что-то пошло не так!"
    
    return render_template("question.html", the_title = "Вспомнить всё", the_question = question_str)

# переключение в режим отладки:
# flask перезапускает веб-приложение когда замечает, что код изменился
if __name__ == "__main__":
    app.run(debug = True)
