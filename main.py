from flask import Flask, redirect, url_for, render_template, g, request
import configparser
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import random

app = Flask(__name__)


# config
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = 'etc/defaults.cfg'
        config.read(config_location)

        app.config['SECRET_KEY'] = config.get('config', 'SECRET_KEY')

        app.config['DEBUG'] = config.get('config', 'debug')
        app.config['ip_address'] = config.get('config', 'ip_address')
        app.config['url'] = config.get('config', 'url')

        app.config['log_file'] = config.get('logging', 'name')
        app.config['log_location'] = config.get('logging', 'location')
        app.config['log_level'] = config.get('logging', 'level')

        app.config['db_location'] = config.get('quiz_db', 'location')
    except:
        print("Couldn't read configs from: ", config_location)


# logging
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024 * 1024 * 10, backupCount=1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)


init(app)
logs(app)


# database
def get_db():
    connection = sqlite3.connect('var/quiz.db')
    cursor = connection.cursor()
    location = app.config['db_location']
    with app.app_context():
        db = getattr(g, 'db', None)
        if db is None:
            db = sqlite3.connect(location)
            g.db = db

            # table 1: quiz
            cursor.execute('drop table if exists quiz')
            cursor.execute('create table quiz (id int, question text, answer text)')
            release_list_1 = [(1, 'question1', 'answer1'),
                              (2, 'question2', 'answer2'),
                              (3, 'question3', 'answer3'),
                              (4, 'question4', 'answer4'),
                              (5, 'question5', 'answer5'),
                              (6, 'question6', 'answer6'),
                              (7, 'question7', 'answer7'),
                              (8, 'question8', 'answer8'),
                              (9, 'question9', 'answer9'),
                              (10, 'question10', 'answer10')]

            cursor.executemany('insert into quiz values (?, ?, ?)', release_list_1)

            # table 2:options
            cursor.execute('drop table if exists options')
            cursor.execute('create table options (id int, option_1 text, option_2 text, option_3 text, option_4 text)')
            release_list_2 = [(1, '1.1', '1.2', '1.3', '1.4'),
                              (2, '2.1', '2.2', '2.3', '2.4'),
                              (3, '3.1', '3.2', '3.3', '3.4'),
                              (4, '4.1', '4.2', '4.3', '4.4'),
                              (5, '5.1', '5.2', '5.3', '5.4'),
                              (6, '6.1', '6.2', '6.3', '6.4'),
                              (7, '7.1', '7.2', '7.3', '7.4'),
                              (8, '8.1', '8.2', '8.3', '8.4'),
                              (9, '9.1', '9.2', '9.3', '9.4'),
                              (10, '10.1', '10.2', '10.3', '10.4'), ]
            cursor.executemany('insert into options values (?, ?, ?, ?, ?)', release_list_2)

            connection.commit()
            cursor.execute('select * from quiz')
            data_quiz = cursor.fetchall()
            cursor.execute('select * from options')
            data_options = cursor.fetchall()

    return data_quiz, data_options


# close db
@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# quiz
# intro page-info.html, also start page
@app.route('/')
def info():
    # check config
    print(app.config['SECRET_KEY'])
    this_route = url_for('info')
    app.logger.info('log info: ' + this_route)
    return render_template('info.html')


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    print('button pressed')
    return redirect(url_for('.home'))


# quiz page
@app.route('/home')
def home():
    data_question, data_options = get_db()

    # random all question and show 5 each time
    quizs = random.sample(data_question, 5)
    ordered_options = []
    for q in quizs:
        for o in data_options:
            if q[0] == o[0]:
                ordered_options.append(o)

    # random options order match question id
    options = []
    for i in ordered_options:
        new_op = [i[0]]
        ops = i[1:10]
        new_op += random.sample(ops, 4)
        options.append(new_op)

    # return options
    return render_template('home.html', quizs=quizs, options=options)


@app.route('/home/<e>/<x>', methods=['POST', 'GET'])
def select(e, x):
    print(x)


# submit quiz
@app.route('/submitquiz', methods=['POST', 'GET'])
def submit():
    correct = 0

    #大致想法
    # for q in quizes
    # q id from data = q id from home.html
    # user choice (value) = request.form[q_id]
    # correct option = answer text in quiz data
    #
    #if user choice ==corect option:
    # correct = correct + 1
    # correct = int(correct)

    return correct


# score page
@app.route('/score')
def score():
    return render_template('score.html')
    # print correct


# error page
@app.errorhandler(404)
def page_not_find(error):
    return 'Opps, page you requested is not exsit yet, please return to previous page.', 404


# run
if __name__ == '__main__':
    init(app)
    app.run()
