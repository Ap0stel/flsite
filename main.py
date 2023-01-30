from flask import Flask, render_template

app = Flask(__name__)

menu = ['Установки', 'Первое приложение' , 'Обратная связь']


@app.route("/")
def index():
    return render_template('index.html', title='Главная', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='О сайте', menu=menu)


@app.route("/about/Pasha")
def pasha():
    return '<h1>Pasha vlojen<h1>'


if __name__ == "__main__":
    app.run(debug=True)
