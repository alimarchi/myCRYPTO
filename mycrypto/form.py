from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from mycrypto.models import DataHandle

def coin_validation(form, field):
    if field.data == form.coin_from.data:
        raise ValidationError("Please select different currencies")

class TransactionsForm(FlaskForm):
    coin_from = SelectField("From: ", validators=[DataRequired(message="Please select one option.")],
    choices=[])
    
    coin_to = SelectField("To: ", validators=[DataRequired(message="Please select one option."), coin_validation],
    choices=['EUR','ETH','BNB','BTC','LUNA','SOL', 'BCH', 'LINK', 'ATOM', 'USDT'])
    
    quantity = FloatField("Quantity: ", validators=[DataRequired(message="Please insert a number"), 
                        NumberRange(message="Please insert a positive quantity", min=0.0001)])

    coin_from_hiddenfield = HiddenField("From: ")
    coin_to_hiddenfield = HiddenField("To: ")
    quantity_hiddenfield = HiddenField("Quantity: ")
    
    quantity_to = FloatField("Quantity: ")
    quantity_to_hidden = HiddenField("Quantity to: ")
    unit_price = FloatField("Unit Price: ")
    
    calculate = SubmitField("Calculate")
    accept = SubmitField("Confirm")
    
