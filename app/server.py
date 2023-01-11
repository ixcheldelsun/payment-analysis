from flask import Flask, request, render_template
from services.user import service as user_service 
from services.payment import service as payment_service
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

from config import settings

server = Flask(__name__)
mysql = MySQL(server)


# config
server.config['MYSQL_HOST'] = settings.MYSQL_HOST
server.config['MYSQL_USER'] = settings.MYSQL_USER
server.config['MYSQL_PASSWORD'] = settings.MYSQL_PASSWORD
server.config['MYSQL_DB'] = settings.MYSQL_DB
server.config['MYSQL_PORT'] = settings.MYSQL_PORT

server.config['MAIL_SERVER']=settings.MAIL_SERVER
server.config['MAIL_PORT'] = settings.MAIL_PORT
server.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
server.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
server.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
server.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL

# email service
mail = Mail(server)

    
@server.route("/register", methods=["POST", "GET"])
def create_user():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if 'password' in request.form and 'email' in request.form :
            password = request.form['password']
            email = request.form['email']
            msg, http_code = user_service.create_user(cur, mysql, email, password)
            return msg, http_code
    else:
        return user_service.get_all_users(cur)
    

@server.route("/payment", methods=["POST", "GET"])
def create_payment():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        return payment_service.get_all_payments(cur)
    elif request.method == 'POST':
        data = request.form
        user_id = user_service.get_user(cur, data["email"])
        if not user_id:
            return "user not found", 404
        return payment_service.create_payment(cur, mysql, user_id, data)     
    
    
@server.route("/payment/<user_email>", methods=["GET"])
def get_payments(user_email):
    cur = mysql.connection.cursor()
    user_id = user_service.get_user(cur, user_email)
    if not user_id:
        return "user not found", 404
    payments_info = payment_service.get_user_payments_summary(cur, user_id)
    msg = Message(
                'Here is your payments summary 💳',
                sender=settings.MAIL_USERNAME,
                recipients = ['ixcheldelsolga@gmail.com']
               )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    msg.html = render_template('summary.html', data=payments_info)
    mail.send(msg)
    return 'Sent', 200

    

if __name__ == "__main__":
    server.run(port=8080, host="0.0.0.0", debug=True)