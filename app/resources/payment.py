from flask import Flask, request
from flask_smorest import Blueprint
from flask.views import MethodView

from flask import Flask, request, render_template
from services.user import service as user_service 
from services.payment import service as payment_service
from flask_mail import Mail, Message


from config import settings


blp = Blueprint("payment", __name__, description="Payments in platform operations")

@blp.route("/")
class Payment(MethodView):
    
    def __init__(self, db):
        super().__init__()
        self.db = db
    
    def get(self):
        cur = self.db.connection.cursor()
        return payment_service.get_all_payments(cur)

    def post(self):
        cur = self.db.connection.cursor()
        data = request.form
        user_id = user_service.get_user(cur, data["email"])
        if not user_id:
            return "user not found", 404
        return payment_service.create_payment(cur, self.db, user_id, data)     
    
    
@blp.route("/<user_email>")
class PaymentSummary(MethodView):
    
    def __init__(self, db, mail):
        super().__init__()
        self.db = db
        self.mail = mail
    
    def get(self, user_email):
        cur = self.db.connection.cursor()
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
        self.mail.send(msg)
        return 'Sent', 200

  
    



