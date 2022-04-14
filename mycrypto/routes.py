from flask import render_template, request, url_for, redirect, flash
from mycrypto import app
from mycrypto.form import TransactionsForm
from mycrypto.convert import CriptoConvert
from mycrypto.models import DataHandle
from datetime import date, datetime
import sqlite3
from mycrypto.errors import APIError

def available_coins_from(form):
    try:
        data_manager = DataHandle()
        wallet = dict(data_manager.get_wallet())
        coins_selection = ["EUR"]
        for key in wallet:
            if wallet[key] > 0:
                coins_selection.append(key)
            print(key, wallet[key])
        
        return coins_selection
    
    except sqlite3.Error as sqlerror:
            flash("An internal error occurred. Please try again later.")
            return render_template("purchase.html", myform=form)

def validate_quantity(form, coin_from_selected, quantity_selected):
    try:
        data_manager = DataHandle()
        wallet = dict(data_manager.get_wallet())
        if coin_from_selected != "EUR" and quantity_selected > wallet[coin_from_selected]:
            flash("Insufficient balance. Please insert a different quantity")
            return render_template("purchase.html", myform=form)
        else: 
            return quantity_selected
    
    except sqlite3.Error as sqlerror:
            flash("An internal error occurred. Please try again later.")
            return render_template("purchase.html", myform=form)

@app.route("/")
def start():
    try:
        data_manager = DataHandle()
        mydata = data_manager.get_data()
        return render_template ("transactions.html", transactions=mydata, empty="NO TRANSACTIONS")
    except sqlite3.Error as sqlerror:
            flash("An internal error occurred. Please try again later.")
            return render_template("transactions.html", transactions=[], empty="NO TRANSACTIONS")

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    form = TransactionsForm()
    form.coin_from.choices = available_coins_from(form)

    if request.method == 'GET':
        return render_template ("purchase.html", myform=form)

    elif request.method == 'POST':
        if form.validate():
            print("pasa por validate")
            value1 = form.coin_from.data
            value2 = form.coin_to.data
            value_quantity = validate_quantity(form, form.coin_from.data, form.quantity.data)
        
            if form.calculate.data:
                try:
                    api = CriptoConvert(value1, value2, value_quantity)
                    value_quantity2 = api.get_conversion()
                    unit_price = round(value_quantity / value_quantity2, 9)
                    form.quantity_to.data = value_quantity2
                    form.quantity_to_hidden.data = value_quantity2
                    form.unit_price.data = unit_price
                    form.coin_from_hiddenfield.data = value1 
                    form.coin_to_hiddenfield.data = value2
                    form.quantity_hiddenfield.data = value_quantity
                    return render_template("purchase.html", myform=form)
                except APIError:
                    flash("The service is currently unavailable. Please try again later.")
                    return render_template ("purchase.html", myform=form)    

            elif form.accept.data:
                if form.quantity_to_hidden.data:
                    if form.coin_from_hiddenfield.data == value1 and form.coin_to_hiddenfield.data == value2 and form.quantity_hiddenfield.data == str(value_quantity):
                        print("la seleccion es correcta")
                        value_quantity_to = form.quantity_to_hidden.data
                        today = str(date.today())
                        current_time = str(datetime.now().time())
                        data_manager = DataHandle()
                        data_manager.set_data((today, current_time, value1, value_quantity, value2, value_quantity_to))
                
                        return redirect(url_for("start"))
                    else:
                        flash("You cannot edit your choices if the value of the transaction has already been calculated. Please try again.")
                        return render_template("purchase.html", myform=form)
                else:
                    flash("Please select Calculate before confirming the transaction.")
                    return render_template("purchase.html", myform=form)
                
        else:
            print("no pasa por validate")
            return render_template("purchase.html", myform=form)
            

@app.route("/status")
def status():
    return render_template ("status.html")

