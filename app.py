from flask import Flask, flash, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"]= r'sqlite:///{cwd}\test.db'.format(cwd=os.path.abspath("."))
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    books= db.relationship('Book')
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(80), unique=True)
    cost = db.Column(db.Float())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    def __init__(self, bookname, cost):
        self.bookname = bookname
        self.cost = cost

    def __repr__(self):
        return '<Book %r>' % self.bookname


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Book=Book)

@app.route('/flash')
def give_flash():
    flash('welcome!')
    return 'flash'

@app.route('/')
def index():
    flash('hello!')
    return  "hello"

@app.route('/users')
def user():
    all_user=User.query.all()
    all_info=[(user,user.books) for user in all_user]
    return render_template("index.html",all_info=all_info)

if __name__ == '__main__':
    app.run()