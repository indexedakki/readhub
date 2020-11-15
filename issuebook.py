
from os import name
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
#from flask_bootstrap import Bootstrap
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from dbmodels import issuebook , contact
#from waitress import serve
import os


flask_app = Flask(__name__, template_folder='html')
#Bootstrap(flask_app)
flask_app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
flask_app.config['SQLALCHEMY_BINDS'] = {
    'contact': 'sqlite:///database/contact.db',
    'issuebook': 'sqlite:///database/issuebook.db'
                                       }
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(flask_app)

@flask_app.before_first_request
def create_tables():
    db.create_all()

@flask_app.route('/')
def Contact():
    return render_template('IssueBook.html')

@flask_app.route('/Contact1', methods=['POST'])
def Contact1():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Phone_Number = request.form.get('Phone_Number')
        Message = request.form.get('Message')
        new_user = contact(Name=Name, Email=Email, Phone_Number=Phone_Number, Message=Message)
        # new_user = User(Email=Email)
        # new_user = User(Phone_Number=Phone_Number)
        # new_user = User(Message=Message)
        db.session.add(new_user)
        db.session.commit()
        return render_template('Contact.html')


@flask_app.route('/IssueBook', methods=['POST'])
def IssueBook():
    if request.method == 'POST':
        # print("taking input")
        Name = request.form.get('Name')
        ISBN = request.form.get('ISBN')
        Title = request.form.get('Title')
        Author = request.form.get('Author')
        Edition = request.form.get('Edition')
        Email = request.form.get('Email')
        print(Name)
        newuser = issuebook(Name=Name, ISBN=ISBN, Title=Title, Author=Author, Edition=Edition, Email=Email)
        db.session.add(newuser)
        db.session.commit()
        # print("submitted")
        return render_template('IssueBook.html')


if __name__ == '__main__':
    flask_app.run(debug = True, port=8501)