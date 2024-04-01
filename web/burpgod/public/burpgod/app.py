from flask import Flask, request, make_response
from os import getenv

FLAG = getenv("FLAG", "krdu{test}")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def challenge():
    # Определение базового HTML шаблона для ответа
    html_template = """
    <html>
    <head>
        <title>BURPGOD</title>
        <style>
            body {{
                background-image: url('{background_url}');
                background-size: cover;
                color: #b31bb0;
                text-align: center;
                padding-top: 20%;
            }}
            h1 {{
                text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff; /* Контур текста */
            }}
        </style>
    </head>
    <body>
        <h1>{message}</h1>
    </body>
    </html>
    """

    # Задаем URL изображений для разных сценариев
    default_background = "./static/1.webp"
    referrer_background = "./static/1.webp"
    user_agent_background = "./static/2.webp"
    wrong_cookie_background = "./static/3.webp"
    admin_false_background = "./static/4.webp"
    wrong_method_background = "./static/5.webp"
    success_background = "./static/6.webp"

    # Проверка и установка куки по умолчанию, если его нет
    role_cookie = request.cookies.get("role")

    if role_cookie is None:
        response = make_response(
            html_template.format(
                background_url=default_background, message="Добро пожаловать!"
            )
        )
        response.set_cookie("role", "dXNlcg==")  # 'user' в Base64
        return response

    # Проверка реферера
    referrer = request.headers.get("Referer")
    if not referrer or "example.com" not in referrer:
        message = (
            'Кажется, вы пришли не с <a href="https://example.com">example.com</a>'
        )
        return make_response(
            html_template.format(background_url=referrer_background, message=message)
        )

    # Проверка User-Agent
    user_agent = request.headers.get("User-Agent", "")
    if user_agent != "venator":
        message = "Ваш браузер не: venator"
        return make_response(
            html_template.format(background_url=user_agent_background, message=message)
        )

    # Дальнейшая логика обработки запроса, начиная с проверки куки...
    if role_cookie != "YWRtaW4=":  # 'admin' в Base64
        message = "Неверные куки."
        return make_response(
            html_template.format(
                background_url=wrong_cookie_background, message=message
            )
        )

    # Проверка заголовка Admin
    is_admin = request.headers.get("Admin") == "true"
    if not is_admin:
        message = "Admin: false."
        return make_response(
            html_template.format(background_url=admin_false_background, message=message)
        )

    # Проверка метода запроса
    if request.method == "GET":
        message = "Неверный метод запроса.  "
        return make_response(
            html_template.format(
                background_url=wrong_method_background, message=message
            )
        )
    elif request.method == "POST":
        message = f"Поздравляем, вы получили флаг: {FLAG}. "
        return make_response(
            html_template.format(background_url=success_background, message=message)
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
