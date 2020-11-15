from flask import Flask, render_template, redirect, url_for, request

from flask_mail import Mail,  Message
flask_app = Flask(__name__, template_folder='html')

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'gesouraus69@gmail.com',
    MAIL_PASSWORD = 'oclodusGe69'
)

mail = Mail(app)
@flask_app.route('/')
def Contact():
    return render_template('Contact.html')

@flask_app.route('/Contact2', methods=['POST'])
def Contact2():
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
    return render_template('Contact.html')
if __name__ == '__main__':
    flask_app.run(debug = True, port=8001)