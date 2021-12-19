from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from flask import render_template, request, redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///this_is_awesome.db'
# Мы связали SQLAlchemy и нашу базочку
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Для вывода результатов, я делала функции, чтобы не запутаться в происходящем
# Количество всего участвовавших + Брейгель
def define_numbers():
    counted_humans = db.session.query(Human).count()
    counted_knowledgers = db.session.query(Human).filter(
        Human.breigel == "да"
    ).count()
    return counted_humans, counted_knowledgers

# Функция для вывода согласующихся слов
def word_final(number):
    numnum = [2,3,4]
    if number % 100 > 4 and number % 100 < 20:
        word0 = "прошло"
        word1 = "человек"
    elif number % 10 in numnum:
        word0 = "прошло"
        word1 = "человека"
    elif number % 10 == 1:
        word0 = "прошел"
        word1 = "человек"
    else:
        word0 = "прошло"
        word1 = "человек"
    return word0, word1

def kringe_function():
    list_of=["На онлайн-уроке химии Вовочка умудрился взорвать онлайн-школу",\
             "В детстве Вовочка любил всех животных, а теперь любит только жатецкого гуся и велкопоповицкого козла",\
             "Работа не волк, волк — это ходить, работа — это ворк",\
             "Анекдоты про Вовочку стали политическими теперь и на Украине",\
             "Падение — это не провал, Провал — это провал, Падение — это где упал"]
    final_number = 0
    final_answer = ""
    for i in list_of:
        countcount = db.session.query(Answer.kringe).filter(
            Answer.kringe == i
        ).count()
        if countcount > final_number:
            final_number = countcount
            final_answer = i
    return final_answer

def fun_function():
    list_of=["На онлайн-уроке химии Вовочка умудрился взорвать онлайн-школу",\
             "В детстве Вовочка любил всех животных, а теперь любит только жатецкого гуся и велкопоповицкого козла",\
             "Работа не волк, волк — это ходить, работа — это ворк",\
             "Анекдоты про Вовочку стали политическими теперь и на Украине",\
             "Падение — это не провал, Провал — это провал, Падение — это где упал"]
    final_number = 0
    final_answer = "голо"
    for i in list_of:
        countcount = db.session.query(Answer.funny).filter(
            Answer.funny == i
        ).count()
        if countcount > final_number:
            final_number = countcount
            final_answer = i
    return final_answer


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/after')
def afterindex():
    return render_template('after.html')

@app.route('/res2')
def res2index():
    numbers_of = define_numbers()
    return render_template('res2.html', vsenum=numbers_of[0], vse2=word_final(numbers_of[0])[0], \
                           vse1=word_final(numbers_of[0])[1], tol=numbers_of[1], KRINGE=kringe_function(),\
                           FUN=fun_function())

@app.route('/questions', methods=["POST", "GET"])
def grindex():
    if request.method == "POST":
         try:
             h = Human(gender=request.form.get('gender'), age=request.form.get('age'), breigel=request.form.get('breigel'))
             db.session.add(h)
             db.session.flush()
             an = Answer(old= str(request.form.getlist('old')), modern= str(request.form.getlist('modern')),
                         memes=request.form.get('memes'), volk=request.form.get('volk'),
                         kringe=request.form.get('kringe'), funny=request.form.get('funny'),
                         answer_id=h.human_id)
             # ДАААААААААААААААААААААYF{EQ
             db.session.add(an)
             db.session.commit()
             print('пожалуйста')
         except Exception as e:
             db.session.rollback()
             print(h.human_id)
             print('date exception', e)
         return redirect("/after")
    return render_template('questions.html')

# У нас всего 3 вида информации => создаем три класса
class Human(db.Model):

    __tablename__ = "humans"

    human_id = db.Column("id_human", db.Integer, primary_key=True)
    gender = db.Column("gender", db.Text)
    age = db.Column("age", db.Text)
    breigel = db.Column("breigel", db.Text)
    # Вообще, его имя пишется, как Breughel, ну мб потом исправлю

    def __repr__(self):
        return f"<users {self.human_id}>"


class Answer(db.Model):

    __tablename__ = "answers"

    useless_id = db.Column('useless_id', db.Integer, primary_key=True)
    answer_id = db.Column('id_answer', db.Integer, ForeignKey('humans.id_human'))

    old = db.Column('old', db.Text)
    modern = db.Column('modern', db.Text)
    memes = db.Column('memes', db.Text)
    volk = db.Column('volk', db.Text)
    kringe = db.Column('kringe', db.Text)
    funny = db.Column('funny', db.Text)

    def __repr__(self):
        return f"<users {self.answer_id}>"


class Question(db.Model):

    __tablename__ = "questions"

    qu_id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('question', db.Text)

    def __repr__(self):
        return f"<users {self.qu_id}>"





# @app.route('/results/', methods=["POST", "GET"])
# def resindex():
#     age = request.form.get('age')
#     return render_template('results.html')

# @app.route('/after/', methods=["POST", "GET"])
# def results():
#     if request.method == "GET":
#         print('ну что такое-то нахуй2')
#         try:
#             h = Human(gender=request.form.get('gender'), age=request.form['age'], breigel=request.form['breigel'])
#             print('ну что такое-то нахуй2')
#             db.session.add(h)
#             db.session.flush()
#
#             a = Answer(old=request.form['old'], modern=request.form['modern'],
#                        memes=request.form['memes'], volk=request.form['volk'],
#                        kringe=request.form['kringe'], funny=request.form['funny'],
#                        answer_id=h.id_human)
#             db.session.add(a)
#             db.session.commit()
#             print('ну что такое-то нахуй')
#         except:
#             db.session.rollback()
#             print(222222222222222222222)
#     return render_template("after.html")

# @app.route('/results')
# def pindex():
#     resultfull1 = Result.query.get()
#
#
#     return render_template('results.html', resfu=resultic1)
#это чтобы вставить ответ

if __name__ == '__main__':
    app.run(debug=True)