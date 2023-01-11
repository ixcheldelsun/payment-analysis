import datetime, os
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from utils import check_credentials, get_user, get_payments_summary
from flask_mail import Mail, Message

from config import settings


server = Flask(__name__)
mysql = MySQL(server)


# config
server.config["MYSQL_HOST"] = settings.MYSQL_HOST
server.config["MYSQL_USER"] = settings.MYSQL_USER
server.config["MYSQL_PASSWORD"] = settings.MYSQL_PASSWORD
server.config["MYSQL_DB"] = settings.MYSQL_DB
server.config["MYSQL_PORT"] = settings.MYSQL_PORT

server.config['MAIL_SERVER']=settings.MAIL_SERVER
server.config['MAIL_PORT'] = settings.MAIL_PORT
server.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
server.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
server.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
server.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL

mail = Mail(server)
    
    
@server.route("/register", methods=["POST", "GET"])
def create_user():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if 'password' in request.form and 'email' in request.form :
            password = request.form['password']
            email = request.form['email']
            # substitute this to create user service
            exists = check_credentials(cur, email)
            if not exists:
                cur.execute(
                    f"INSERT INTO users VALUES (NULL, % s, % s);", (email, password)
                )
                mysql.connection.commit()
                return "user created successfully", 201
            else:
                return "email already used", 400
    else:
        cur.execute("SELECT email FROM users;")
        users = cur.fetchall()
        return str(users), 200
    


@server.route("/payment", methods=["POST", "GET"])
def create_payment():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT user, amount, DATE_FORMAT(date_created, '%d %m %Y')  FROM payments;")
        payments = cur.fetchall()
        return str(payments), 200
    elif request.method == 'POST':
        data = request.form
        # substitute this to create user service
        cur = mysql.connection.cursor()
        user_id = get_user(cur, data["email"])
        cur.execute(
            f"""INSERT INTO payments VALUES (NULL, %s, %s, %s)""", 
            (user_id, data["amount"], datetime.datetime.utcnow(),)
        )
        mysql.connection.commit()
        return "payment created successfully", 201
    
    
@server.route("/payment/<user_email>", methods=["GET"])
def get_payments(user_email):
    cur = mysql.connection.cursor()
    payments_info = get_payments_summary(cur, user_email)
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