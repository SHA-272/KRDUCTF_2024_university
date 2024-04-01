from functools import wraps
from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

def check_login(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user

def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt')
        if not token or not verify_jwt(token):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_login(username, password)
        if user:
            token = jwt.encode({'user': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
            response = make_response(redirect(url_for('admin_page')))
            response.set_cookie('jwt', token, httponly=True)
            return response
        else:
            return "Unauthorized", 401
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')

@app.route('/chief', methods=['GET', 'PUT'])
@login_required
def chief_page():
    if request.method == 'PUT':
        token = request.cookies.get('jwt')
        payload = verify_jwt(token)

        if payload and 'user' in payload and payload['user'] == "admin":
            message = "Флаг: krdu{B3$T_h4ck3r_v_$hk0l3}"
            flag = True
        else:
            message = "Отказано в доступе"
            flag = False
    else:  # Обработка GET-запроса
        message = "Неверный метод запроса"
        flag = False

    return render_template('chief.html', message=message, flag=flag)

@app.route('/protocol1111')
@login_required
def protocol():
    return render_template('protocol.txt')

if __name__ == '__main__':
    app.run(debug=True, port=7000)
