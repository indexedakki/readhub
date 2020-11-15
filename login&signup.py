from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
#from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from dbmodels import User

from wtforms import ValidationError
import os


flask_app = Flask(__name__, template_folder='html')
#Bootstrap(flask_app)
flask_app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    

@flask_app.route('/LoginPage')
def login():
    return render_template('LoginPage.html')

# @flask_app.route('/SignupPage')
# def signup():
#     return render_template('SignupPage.html')

# @flask_app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))    # url_for takes function Name as argument

@flask_app.route('/')
def index():
    return render_template('SignupPage.html')




@flask_app.route('/LoginPage', methods=['GET','POST'])
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

@flask_app.route('/LoginPage1')
def home():
    return render_template('home.html')





@flask_app.route('/SignupPage', methods=['GET','POST'])
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
    

if __name__ == '__main__':
    flask_app.run(debug = True, port=8501)