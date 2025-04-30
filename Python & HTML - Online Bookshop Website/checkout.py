from flask import Flask, flash,url_for, request, redirect,make_response
from flask import session, Blueprint, render_template, g, abort
from markupsafe import escape
from flask_wtf import Form
from pathlib import Path
from wtforms import StringField, PasswordField, TextAreaField,IntegerField,FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange,DataRequired, Length
from flask_uploads import configure_uploads, IMAGES, UploadSet
import functools
import sqlite3

checkout = Blueprint("checkout", __name__)

class CheckoutForm(Form):
  name = StringField('Name on Card', validators=[InputRequired()])
  cnumber = IntegerField('Card Number', validators=[InputRequired()])
  exp = DateField('Expiration Date', format='%Y-%m', validators=[InputRequired()])
  cvv = StringField('CVV', validators=[InputRequired(), Length(min=3,max=3)])

@checkout.route('/complete_order')
def complete_order():
  """ This route renders the checkout.html if there are enough books in stock to prooceed with the payment. 
  If there is not enough, return back to cart.html with an error """
  if 'username' in session: #checks if user is logged in
    if 'cart_item' in session: #checks if cart is in session
        return render_template("complete_order.html", error=check_stock(), postage=postage())
    else:
      return render_template(url_for('index'))
  else:
    return redirect(url_for('register_login.login'));
    
def check_stock():
  try:
    #connect to the book stock database
    con = sqlite3.connect('book_stock.db')
    cursor = con.cursor();
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    session.modified=True

    for row in rows: #for each book in the book stock database
      for item in session['cart_item'].items():
        if int(row[0]) == int(item[0]): # check if a book in the book stock database has the same isbn as an item in cart
          if session['cart_item'][item[0]]['quantity'] > int(row[8]): #check if the quantity in cart is greater than the stock available for the book
            session['all_total_price'] = session['all_total_price'] - session['cart_item'][item[0]]['total_price'] 
            session['all_total_quantity'] = session['all_total_quantity'] - session['cart_item'][item[0]]['quantity']
            session['cart_item'][item[0]]['quantity'] = int(row[8])
            session['cart_item'][item[0]]['total_price'] = int(session['cart_item'][item[0]]['price'])*int(session['cart_item'][item[0]]['quantity'])
            session['all_total_price'] = session['all_total_price'] + session['cart_item'][item[0]]['total_price']
            session['all_total_quantity'] = session['all_total_quantity'] + int(session['cart_item'][item[0]]['quantity'])
            error="Not enough stock", item[0]
            return error
  finally:
    cursor.close()
    con.close()

def postage():
  postage_cost = 2
  for item in session['cart_item'].items():
    postage_cost = postage_cost + session['cart_item'][item[0]]['quantity']
  session['postage'] = postage_cost
  return postage_cost

@checkout.route('/checkout', methods=['GET','POST'])
def check_out():
  if 'username' in session: #checks if user is logged in
    if 'cart_item' in session:
      if request.method == 'POST':
        return adjust_stock()
      else:
        return show_checkout_form()
    else:
      return render_template(url_for('index'))
  else:
    return redirect(url_for('register_login.login'));

def show_checkout_form():
  form = CheckoutForm()
  if form.validate_on_submit():
    print('Paid successfully')
  return render_template("checkout.html", form=form)

def adjust_stock():
  try:
    con = sqlite3.connect('book_stock.db')
    cursor = con.cursor();
    cursor.execute("SELECT * FROM books")
    print('connected')
    books = cursor.fetchall()
    session.modified=True
    
    for key, value in session['cart_item'].items():
      for book in books:
        print('looped')
        if book[0] == int(key):
          print('equal key')
          new_stock = book[8] - session['cart_item'][key]['quantity']
          cursor.execute('UPDATE books SET quantity=? WHERE isbn=?',(new_stock, book[0]))
          con.commit()
          
    all_total_price = 0
    all_total_quantity = 0

    for key in list(session['cart_item'].keys()):
      session['cart_item'].pop(key)

    session['all_total_quantity'] = all_total_quantity
    session['all_total_price'] = all_total_price
    paid = "You have succesfully paid"
    return redirect(url_for('index'))
  finally:
    cursor.close()
    con.close()