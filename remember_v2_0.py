from flask import Flask, render_template, request
import json
import os


class Remember:
    data = {}  # словарь вопросов
    current_course = ""
    current_question = 1
    last_question = 1
    status = 200

    def __init__(self) -> None:
        if os.path.exists("templates/remember.html"):
            os.remove("templates/remember.html")
        self.load_dict()
        if self.status == 200:
            self.generate_index()

    def load_dict(self) -> None:
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    self.data = json.load(f)
            except Exception as e:
                self.status = 404
        else:
            self.status = 404

    def generate_index(self):
        page = "{% extends 'base.html' %}\n"
        page += "{% block body %}\n"
        page += "    <form method='POST' action='/question'>\n"
        page += "        <table>\n"
        for course, questions in self.data.items():
            page += "            <tr>\n"
            page += f"                <td class='questions name_questions'>{course}</td>\n"
            page += f"                <td class='questions counts_questions'>{len(questions)}</td>\n"
            page += f"                <td><input class='edit' name='edit_{course}' type='TEXT' value='' maxlength='4' placeholder='Номер' size='4' pattern='[0-9]+'></td>\n"
            page += f"                <td><input class='btn' name='btn_{course}' type='SUBMIT' value='Ok'></td>\n"
            page += "            </tr>\n"
        page += "        </table>\n"
        page += "    </form>\n"
        page += "{% endblock %}"
        try:
            with open("templates/remember.html", "w", encoding="utf-8") as f:
                f.write(page)
        except Exception as e:
            self.status = 404
            return

    def reset_state(self):
        self.current_course = ""
        self.current_question = 1
        self.last_question = 1
        self.status = 200


app = Flask(__name__)
A = Remember()


@app.route("/")
def hello() -> str:
    return "Hello from Flask!"

"""
The canonical URL for the 'remember' endpoint has a trailing slash. It's similar to a folder in a file system.
If you access the URL without a trailing slash ('/remember'), Flask redirects you to the canonical URL with
the trailing slash ('/remember/').
"""
@app.route("/remember/")
def index() -> str:
    """
    Обработчик начальной страницы
    :return: web-страница
    """
    A.reset_state()
    return render_template("remember.html", the_title = "Вспомнить всё")


@app.route("/question", methods=["POST"])
def question():
    res = {}
    if len(request.form) != 0:
        btn = ""
        edit = ""
        question_str = ""
        for k, v in request.form.items():
            # k - имя элемента input - кнопки или поля ввода и пр.
            # v - надпись на кнопке или содержание поля ввода
            res[k] = v
            if k[:3] == "btn":
                btn = k
                continue
            if k[:4] == "edit" and v != "":
                edit = k
        if btn == "" and edit == "":
            # здесь уже выбран курс и показан вопрос, переход на следующий вопрос
            # получаю словарь первого курса как список и там 0-й элемент
            v = list(A.data.values())[0]
            if (A.current_question + 1) > A.last_question:
                A.current_question = 1
            else:
                A.current_question += 1
        else:
            A.current_course = btn[4:]
            # A.data[A.current_course].keys() - динамическое отображение ключей,
            # т.е. вопросов текущего курса
            # reversed - превращаю в инвертированный итератор, т.е. с конца
            # и из списка беру 0-й элемент, который является последним номером вопроса в данном курсе
            A.last_question = int(list(reversed(A.data[A.current_course].keys()))[0])
            if A.current_course == edit[5:]:
                # введен номер вопроса и нажата кнопка соответствующего курса
                A.current_question = int(res[edit])
            else:
                # нажата кнопка без номера вопроса или
                # кнопка другого курса чем номер вопроса
                A.current_question = 1
        question_str = f"{A.current_question}. {A.data[A.current_course][str(A.current_question)]}"
        return render_template("question.html",
                               the_title="Начальная страница",
                               the_question=question_str)
    else:
        return "Empty form!"


if __name__ == "__main__":
    app.run(debug=False)
