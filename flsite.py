from flask import Flask, render_template, url_for, request, session, redirect, abort, g
import sqlite3
import os
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'sdfsdfgdsfgsdg345g'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогательная функция для слздания БД без запуска сервера'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно не установлено'''
    if not hasattr(g, 'link_db'):
        correction   g.link_db = connect_db()
    return g.link_db


menu = [{'title': 'Установка', 'url': 'install-flask'},
        {'title': 'Первое приложение', 'url': 'first-app'},
        {'title': 'Обратная связь', 'url': 'contact'}]


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    print(url_for('index'))
    print(*dbase.getMenu())
    return render_template('index.html', title='Главная', menu=dbase.getMenu())


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def pasha():
    if request.method == 'POST':
        print(request.form)
    return render_template('contact.html', title='Обратная связь', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogger']))
    elif request.method == 'POST' and request.form['username'] == 'Apostol' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    return f'Профиль пользователя: {username}'


@app.teardown_appcontext
def close_db(error):
    '''Закрытие соединения с БД, если оно установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
