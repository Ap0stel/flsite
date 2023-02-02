from flask import Flask, render_template, url_for, request, session, redirect, abort, g, flash
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
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
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)



@app.route("/")
def index():
    print(url_for('index'))
    print(*dbase.getMenu())
    return render_template('index.html', title='Главная', menu=dbase.getMenu())


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=dbase.getMenu())


@app.route('/contact', methods=['POST', 'GET'])
def pasha():
    if request.method == 'POST':
        print(request.form)
    return render_template('contact.html', title='Обратная связь', menu=dbase.getMenu())


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogger']))
    elif request.method == 'POST' and request.form['username'] == 'Apostol' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', menu=dbase.getMenu())


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    return f'Профиль пользователя: {username}'


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи1', category = 'error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи2', category='error')

    return render_template('add_post.html', menu = dbase.getMenu(), title="Добавление статьи")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4\
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('вы успешно зарегистрировались', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД - 1', 'error')
        else:
            flash('Неверно заполнены поля', 'error')
    return render_template('register.html', menu=dbase.getMenu(), title='Регистрация')





@app.teardown_appcontext
def close_db(error):
    '''Закрытие соединения с БД, если оно установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
