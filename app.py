
from os import name
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
#from flask_bootstrap import Bootstrap
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from dbmodels import issuebook , contact, User
#from waitress import serve
import os

#from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from wtforms import ValidationError

from flask_mail import Mail,  Message


flask_app = Flask(__name__, template_folder='html')
#Bootstrap(flask_app)
flask_app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
flask_app.config['SQLALCHEMY_BINDS'] = {
    'contact': 'sqlite:///database/contact.db',
    'issuebook': 'sqlite:///database/issuebook.db'
                                       }
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


flask_app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'gesouraus69@gmail.com',
    MAIL_PASSWORD = 'oclodusGe69'
)
mail = Mail(flask_app)

db.init_app(flask_app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(flask_app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


"""
Routes
"""

@flask_app.before_first_request
def create_tables():
    db.create_all()

@flask_app.route('/')
def Contact():
    return render_template('SignupPage.html')

@flask_app.route('/SignupPagePost', methods=['GET','POST'])
def signup_post():
    Name = request.form.get('Name')
    Email = request.form.get('Email')
    Password = request.form.get('Password')
    Phone = request.form.get('Phone')
    # Gender = request.form.get('Gender')
    user = User.query.filter_by(Email=Email).first() # if this returns a user, then the Email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')    

        return render_template('blank2.html')

    # create new user with the form data. Hash the Password so plaintext version isn't saved.
    new_user = User(Email=Email, Name=Name, Password=generate_password_hash(Password, method='sha256'), Phone=Phone)
    #Password=generate_password_hash(Password, method='sha256')
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    print("form Submitted")
    return render_template('blank3.html')

@flask_app.route('/LoginPagePre')
def login_pre():
    return render_template("/Loginpage.html")


@flask_app.route('/SignupPagePre')
def NewUser():
    return render_template("/SignupPage.html")

@flask_app.route('/LoginPagePost', methods=['GET','POST'])
def login_post():
    Email = request.form.get('Email')
    Password = request.form.get('Password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(Email=Email).first()
    
    # check if user actually exists
    # take the user supplied Password, hash it, and compare it to the hashed Password in database
    if not user or not check_password_hash(user.Password, Password):
        flash('Please check your login details and try again.')
        print("user doesnt exists")
        return render_template("blank.html") # if user doesn't exist or Password is wrong, reload the page
    print("user exists")
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return render_template("home.html")


@flask_app.route('/Contact')
def preContact():
    return render_template('Contact.html')

@flask_app.route('/postContact', methods=['POST'])
def postContact():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Phone_Number = request.form.get('Phone_Number')
        Message = request.form.get('Message')
        mssg="Name: "+ Name + "\nEmail: " +Email + "\nPhone:" + Phone_Number + "\nMessage:" + Message
        msg = mail.send_message(
        'FeedBack',
        sender='gesouraus69@gmail.com',
        recipients=['gesouraus69@gmail.com'],
        body= mssg
    )
    return render_template('blank4.html')
        # Name = request.form.get('Name')
        # Email = request.form.get('Email')
        # Phone_Number = request.form.get('Phone_Number')
        # Message = request.form.get('Message')
        # new_user = contact(Name=Name, Email=Email, Phone_Number=Phone_Number, Message=Message)
        # # new_user = User(Email=Email)
        # # new_user = User(Phone_Number=Phone_Number)
        # # new_user = User(Message=Message)
        # db.session.add(new_user)
        # db.session.commit()
        # return render_template('Contact.html')

@flask_app.route('/preIssueBook')
def preIssueBook():
    return render_template('IssueBook.html')

@flask_app.route('/postIssueBook', methods=['POST'])
def postIssueBook():
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

# @flask_app.route('/SendMail', methods=['POST'])
# def Contact2():
#     Name = request.form.get('Name')
#     Email = request.form.get('Email')
#     Phone_Number = request.form.get('Phone_Number')
#     Message = request.form.get('Message')
#     mssg="Name: "+ Name + "\nEmail: " +Email + "\nPhone:" + Phone_Number + "\nMessage:" + Message
#     msg = mail.send_message(
#         'FeedBack',
#         sender='gesouraus69@gmail.com',
#         recipients=['gesouraus69@gmail.com'],
#         body= mssg
#     )
#     return render_template('blank4.html')

@flask_app.route('/home')
def homepage():
    return render_template('home.html')

@flask_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_pre')) 


if __name__ == '__main__':
    flask_app.run(debug = False)