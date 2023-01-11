from flask import Flask, request
from flask_smorest import Blueprint
from flask.views import MethodView


blp = Blueprint("payment", __name__, url_prefix="/payment", describe="Payments in platform operations")


class Payment(MethodView):
    def get(self):
        return "get payment"

    def post(self):
        return "post payment"

