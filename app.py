from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '76e911246c2fea24ac29492371be3534c914da7765fc0a49843fa5909697029e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/budget_db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Model transakcji
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

# Model użytkownika
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Funkcja inicjująca bazę danych
def init_app():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_app()
    app.run(debug=True)
