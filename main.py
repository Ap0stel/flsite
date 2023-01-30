from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfsdfgdsfgsdg345g'

menu = [{'name': 'Установка', 'url': 'install-flask'},
        {'name': 'Первое приложение', 'url': 'first-app'},
        {'name': 'Обратная связь', 'url': 'contact'}]


@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', title='Главная', menu=menu)


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
    return render_template('page404.html', title='Страница не найдена',  menu=menu)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogger']))
    elif request.method == 'POST' and request.form['userLogged'] == 'Apostol' and request.form['psw'] == '123':
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', menu=menu)




if __name__ == "__main__":
    app.run(debug=True)
