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

            # table 1: quiz saved as (id, question, correct answer)
            cursor.execute('drop table if exists quiz')
            cursor.execute('create table quiz (id int, question text, answer text)')
            release_list_1 = [(1, 'In which year was the "18-hole" game created?', '1764'),
                              (2, 'Which golf club is normally the longest? (without modification)', 'The 1-wood'),
                              (3, 'In golf, par is the predetermined number of strokes that a proficient golfer '
                                  'should require to complete a hole, you now finished a hole two strokes under the '
                                  'par, what term should you use for your score?', 'Eagle'),
                              (4, 'How many golf clubs can you take with you in a normal  match?', '14'),
                              (5, 'Under what circumstances will a golfer be disqualified?', 'None of these'),
                              (6, 'Where was the modern game of golf originated?', 'Scotland'),
                              (7, 'Which of the following materials has never been used in the manufacture of golf '
                                  'balls ', 'Aluminium'),
                              (8, 'When did manufacturers start using metal for their clubs?', '1979'),
                              (9, 'How grass is usually mowed on a modern greens', 'Shorter'),
                              (10, 'Which is the oldest golf course in the world?', 'The Old Course')]

            cursor.executemany('insert into quiz values (?, ?, ?)', release_list_1)

            # table 2:options saved as (id, choice1, choice2, choice3, choice4)
            cursor.execute('drop table if exists options')
            cursor.execute('create table options (id int, option_1 text, option_2 text, option_3 text, option_4 text)')
            release_list_2 = [(1, '1764', '1874', '1648', '2000'),
                              (2, 'The 1-wood', 'The 5-iron', 'The 9-iron', 'The Putter'),
                              (3, 'Eagle', 'Birdie', 'Bogey', 'Albatross'),
                              (4, '14', '6', '12', 'As many as you want'),
                              (5, 'None of these', 'Making a stroke at the wrong ball', 'A lost ball or a ball hit out of bounds', 'Hitting a fellow player\'s ball if both balls lay on the green prior to the stroke'),
                              (6, 'Scotland', 'USA', 'France', 'USSR'),
                              (7, 'Aluminium', 'Feather', 'Resin', 'Polyurethane'),
                              (8, '1979', '1879', '2000', '1890'),
                              (9, 'Shorter', 'Longer', 'Same as everywhere else', 'Undulating'),
                              (10, 'The Old Course', 'Mission Hills Golf Club', 'Musselburgh Links', 'Pinehurst Resort'), ]
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

    # Difficulties encountered: Unable to get a valid user selection data and transfer from home.html to server side

    # Ideas for scoring functions
    # for q in quizes
    # q id from data = q id from home.html
    # user choice (value) = request.form[q_id]
    # correct option = answer text in quiz data
    #
    # if user choice ==corect option:
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
