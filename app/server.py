import datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from utils import check_credentials

from config import settings


server = Flask(__name__)
mysql = MySQL(server)


# config
server.config["MYSQL_HOST"] = settings.MYSQL_HOST
server.config["MYSQL_USER"] = settings.MYSQL_USER
server.config["MYSQL_PASSWORD"] = settings.MYSQL_PASSWORD
server.config["MYSQL_DB"] = settings.MYSQL_DB
server.config["MYSQL_PORT"] = settings.MYSQL_PORT
    
    
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
    


@server.route("/payment", methods=["POST"])
def create_payment():
    # if 'token' in request.form:
    #     token = request.form['token']
    #     try:
    #         data = jwt.decode(token, server.config["SECRET_KEY"], algorithms=["HS256"])
    data = request.form
    # substitute this to create user service
    cur = mysql.connection.cursor()
    cur.execute(
        f"INSERT INTO payments (email, amount, date_created) VALUES ({data['email']}, {data['amount']}, {datetime.datetime.utcnow()});"
    )
    mysql.connection.commit()
    return "payment created successfully", 200
    #     except:
    #         return "invalid token", 400
    # return "token not found", 400
    

if __name__ == "__main__":
    server.run(port=8080, host="0.0.0.0", debug=True)