from flask import Flask, request, render_template
from services.user import service as user_service 
from services.payment import service as payment_service
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from flasgger import Swagger
from flask_restful import Api, Resource

from config import settings
import json

app = Flask(__name__)
api = Api(app)
mysql = MySQL(app)
swagger = Swagger(app, template=settings.SWAGGER_TEMPLATE)

# config
app.config['MYSQL_HOST'] = settings.MYSQL_HOST
app.config['MYSQL_USER'] = settings.MYSQL_USER
app.config['MYSQL_PASSWORD'] = settings.MYSQL_PASSWORD
app.config['MYSQL_DB'] = settings.MYSQL_DB
app.config['MYSQL_PORT'] = settings.MYSQL_PORT

app.config['MAIL_SERVER']=settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL

# email service
mail = Mail(app)

# apis    
@app.route("/register", methods=["POST", "GET"])
def create_user():
    """Endpoint to create a user given an email and password.
    
    responses:
      201:
        description: 
        schema: user has been created correctly.
    """
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if 'password' in request.form and 'email' in request.form :
            password = request.form['password']
            email = request.form['email']
            msg, http_code = user_service.create_user(cur, mysql, email, password)
            return msg, http_code
    else:
        cur = mysql.connection.cursor()
        data, http_code = user_service.get_all_users(cur)
        return json.dumps(data), http_code
        
    

@app.route("/payment", methods=["POST", "GET"])
def create_payment():
    """Endpoint to create a user given an email and password."""
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        data, http_code = payment_service.get_all_payments(cur)
        data = [{"user": element[0], "amount": element[1], "date": element[2]} for element in data]
        return data, http_code
    elif request.method == 'POST':
        data = request.form
        user_id = user_service.get_user(cur, data["email"])
        if not user_id:
            return "user not found", 404
        return payment_service.create_payment(cur, mysql, user_id, data)     
    
    
@app.route("/payment/<user_email>", methods=["GET"])
def get_payments(user_email):
    cur = mysql.connection.cursor()
    user_id = user_service.get_user(cur, user_email)
    if not user_id:
            return "user not found", 404
    payments_info = payment_service.get_user_payments_summary(cur, user_id)
    msg = Message(
                'Here is your payments summary 💳',
                sender=settings.MAIL_USERNAME,
                recipients = [user_email]
               )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    msg.html = render_template('summary.html', data=payments_info)
    mail.send(msg)
    return 'Sent', 200

# Documentation

class User(Resource):
    def get(self):
        """
        List of registered users.
        ---
        responses:
          200:
            description: List of registered users.
            schema:
                properties:
                    email:
                        type: string
                        description: Email used by user to register.
                        default: test@gmail.com
        """
        return user_service.get_all_users(mysql.connection.cursor())
    
    def post(self):
        """Create a user.
        ---
        parameters:
            -  name: email
               in: formData
               type: string
               required: true
            -  name: password
               in: formData
               type: string
               required: true
              
        responses:
            201:
                description: User created successfully.
            400:
                description: Bad request. User already exists.
        """
        return "User created", 201
    
    
class Payment(Resource):
    def get(self):
        """List of payments done by users.
        ---
        responses:
            200:
                description: A list of payments done by users.
                schema:
                    properties:
                        user_id:
                            type: integer
                            description: id of user who made the transaction.
                            default: 1
                        amount:
                            type: string
                            description: amount of the transaction. If > 0, payment was credit. If < 0, payment was debit.
                            default: -10
                        date:
                            type: string
                            description: date of purchase.
                            default: 10 10 2000
        """
        return payment_service.get_all_payments(mysql.connection.cursor())

    
    def post(self):
        """Create a payment.
        ---
        parameters:
            -  name: email
               in: formData
               type: string
               required: true
            -  name: amount
               in: formData
               type: string
               required: true
              
        responses:
            201:
                description: Payment created successfully.
        """
        return "User created", 201
    

class PaymentSummary(Resource):
    def get(self):
        """Summary of all payments made by user.
        ---
        parameters:
            -   in: path
                name: user_email
                type: string
                required: true
        responses:
            200:
                description: Summary of all payments made by user. An email should be received to the user's provided email address.
            400:
                description: User does not exist.
        """
        return payment_service.get_all_payments(mysql.connection.cursor())


api.add_resource(User, '/register')
api.add_resource(Payment, '/payment')
api.add_resource(PaymentSummary, '/payment/<user_email>')
    

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)