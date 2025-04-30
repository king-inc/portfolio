from flask import Flask, flash,url_for, request, redirect,make_response
from flask import session, Blueprint, render_template, g, abort
from markupsafe import escape
from flask_wtf import Form
from pathlib import Path
import functools
import sqlite3
import numpy as np


shopping = Blueprint("shopping", __name__)

@shopping.route('/add', methods=['POST'])
def add_to_cart():
  if 'username' in session:
    try:
      #request the quantity and isbn number of the book being added to cart
      _quantity =  int(request.form['quantity'])
      _isbn = request.form['isbn']

      if _quantity and _isbn and request.method == 'POST':
        con = sqlite3.connect('book_stock.db')
        cur = con.cursor();
        cur.execute("SELECT * FROM books WHERE isbn=?;", [_isbn])
        row = cur.fetchone()
        itemArray = { _isbn: {'name' : row[1],'isbn':row[0], 'image' : row[5], 'price' : row[7], 'quantity' : _quantity, 'total_price' : _quantity * row[7]}}
        print(type(itemArray))
        print('itemArray is', itemArray)

        all_total_price = 0
        all_total_quantity = 0

        session.modified = True

        if 'cart_item' in session:
          print('in session')
          if _isbn in session['cart_item']:
            for key, value in session['cart_item'].items():
              if _isbn == key:
                total_quantity = session['cart_item'][key]['quantity'] + _quantity
                session['cart_item'][key]['quantity'] = total_quantity
                session['cart_item'][key]['total_price'] = total_quantity * row[7]
          else:
            session['cart_item'].update(itemArray)

          # loop through item cart and add the total amount and price of the books  
          for key, value in session['cart_item'].items():
            individual_quantity = int(session['cart_item'][key]['quantity'])
            individual_price = int(session['cart_item'][key]['total_price'])
            all_total_quantity = all_total_quantity +individual_quantity
            all_total_price = all_total_price + individual_price

        else:
          #set the item being added into session
          session['cart_item'] = itemArray
          all_total_quantity = all_total_quantity + _quantity
          all_total_price = all_total_price + (_quantity*row[7])

        session['all_total_price'] = all_total_price
        session['all_total_quantity'] = all_total_quantity

        return redirect(url_for('index'))
      else:
        return 'Error while adding item to cart'
    except Exception as e:
      print(e)
    finally:
      cur.close()
      con.close()
  else:
    return redirect(url_for('register_login.login'));
    
    
@shopping.route("/cart")
def cart():
  if 'username' in session:
    return render_template("cart.html")
  else:
    return redirect(url_for('register_login.login'));
  

@shopping.route('/clear_cart')
def clear_cart():
  if 'username' in session:
    try:
      all_total_price = 0
      all_total_quantity = 0
      session.modified = True;

      for key in list(session['cart_item'].keys()):
        session['cart_item'].pop(key)

      session['all_total_quantity'] = all_total_quantity
      session['all_total_price'] = all_total_price
      return redirect(url_for('index'))
    except Exception as e:
      print(e)
  else:
    return redirect(url_for('register_login.login'));
  
    
@shopping.route('/delete/<string:isbn>')
def delete_book(isbn):
  if 'username' in session:
    try:
      all_total_price = 0
      all_total_quantity = 0
      session.modified = True;

      for item in session['cart_item'].items():
        if item[0] == isbn:
          if int(session['cart_item'][item[0]]['quantity']) == 1:
            session['cart_item'].pop(item[0],None)
          else:
            session['cart_item'][item[0]]['quantity'] = int(session['cart_item'][item[0]]['quantity']) - 1
            session['cart_item'][item[0]]['total_price'] = int(session['cart_item'][item[0]]['price'])*int(session['cart_item'][item[0]]['quantity'])
          if 'cart_item' in session:
            for key, value in session['cart_item'].items():
              individual_quantity = int(session['cart_item'][key]['quantity'])
              individual_price = int(session['cart_item'][key]['total_price'])
              all_total_quantity = all_total_quantity + individual_quantity
              all_total_price = all_total_price + individual_price
          break

      session['all_total_quantity'] = all_total_quantity
      session['all_total_price'] = all_total_price
      return redirect(url_for('index'))
    except Exception as e:
      print(e)
  else:
    return redirect(url_for('register_login.login'));
  
