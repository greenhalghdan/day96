from flask import Flask, render_template, url_for, redirect, flash
from wtforms import SubmitField
import requests
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anotveryrandomstringofletters'
bootstrap = Bootstrap(app)


class truefalse(FlaskForm):
    truebutton = SubmitField("True")
    falsebutton = SubmitField("False")


@app.route('/', methods=["GET", "POST"])
def index():
    running = True
    while running:
        print('im in the loop')
        questions = requests.get('https://opentdb.com/api.php?amount=10&category=28&type=boolean')
        questiondata = questions.json()
        if questiondata['response_code'] == 0:
            running = False
        else:
            sleep(2)
    i = 0
    print(i)
    print(questiondata)
    question = questiondata["results"][i]['question']
    print(question)
    answer = questiondata["results"][i]['correct_answer']
    trueorfalse = truefalse()
    if trueorfalse.validate_on_submit():
        print(i)
        print(question)
        print(answer)
        rightorwrong = False
        if trueorfalse.truebutton.data:
            if answer == 'True':
                rightorwrong = True
        elif trueorfalse.falsebutton.data:
            if answer == 'False':
                rightorwrong = True
        else:
            print('something else happened')

        if rightorwrong:
            flash('Correct')
        elif not rightorwrong:
            flash('Incorrect')

    return render_template("index.html", question_data = question, form = trueorfalse)


if __name__ == "__main__":
    app.run(debug=True)