from flask import Flask, render_template, request, make_response
import requests, os, json, random

app = Flask(__name__)


# Главная страница
@app.route("/")
def index():
    return render_template("index.html")


# Страница с самораспаковывающимся архивом
@app.route("/888d0ee361af3603736f32131e7b20a2")
def archive():
    return render_template("archive.html")


# Страница с музыкой Лэйн
@app.route("/d189031947db67dd16c3c2b502f55ca2")
def lain():
    return render_template("lain.html")


# Страница главного этапа
@app.route("/0876b6b0db0707db221a5c736d8a896a")
def layer():
    with open("./static/files/dump", "rb") as f:
        file = f.read().decode("utf-8")
        return render_template("layer.html", file=file)


# Страница с флагом
@app.route("/c41b7593c47b29e10d0898cab0c7ba05")
def flag():
    return render_template("flag.html")


# Страница с ошибкой 404 и обработчиком ошибок 404 для отображения ошибки 404 на странице задачи
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Запуск приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
