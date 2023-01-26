from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fgfghjjfghj567jhj'
menu = ['About Me', 'About Russia', 'About my grip']


@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title='О себе', menu=menu)

@app.route('/profile/<path:username>')
def profile(username):
    return f'Пользователь: {username}'


@app.route("/about/Pasha")
def pasha():
    return '<h1>Pasha vlojen<h1>'

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu)



if __name__ == "__main__":
    app.run(debug=True)


