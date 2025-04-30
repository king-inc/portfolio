from flask import Flask, flash,url_for, request, redirect,make_response
from flask import session, Blueprint, render_template, g, abort
from markupsafe import escape
from flask_wtf import Form
from pathlib import Path
from wtforms import StringField, PasswordField, TextAreaField,IntegerField,FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange,DataRequired
from flask_uploads import configure_uploads, IMAGES, UploadSet
import functools
import sqlite3



stock = Blueprint("stock",__name__) #this identifies this file as an add-on to driver file
images = UploadSet('images', IMAGES) #specifies the type of  files to be uploads



#AddForm class specifies the fields to inputted to add a new book to the database
class AddForm(Form):
    bkname = StringField('Name of Book', validators=[InputRequired()])
    author = StringField('Author of Book', validators=[InputRequired()])
    date = DateField('Publication Date', format='%Y-%m-%d', validators=[InputRequired()])
    desc = TextAreaField('Book Description', validators=[InputRequired()])
    image = FileField('Front Cover',validators=[DataRequired()])
    
    
    

@stock.route('/stock_level')
#reference aula shopping cart material
def stock_level():
    if 'username' in session and session['username'] == 'admin':
        if Path("book_stock.db").exists(): # this checks if the book stock database exists
            try:
                con = sqlite3.connect('book_stock.db')
                cursor = con.cursor();
                cursor.execute("SELECT * FROM books")
                rows = cursor.fetchall()
                return render_template('stock.html', books=rows, Path=Path)
            except Exception as e:
                print(e);
            finally:
                cursor.close()
                con.close()    
        else:
            return render_template('stock.html',Path=Path)
    else:
        return redirect(url_for('index'));

@stock.route('/add_stock', methods=['GET','POST'])
def add_stock():
  if 'username' in session and session['username'] == 'admin':
    form = AddForm() #instatiates the AddForm class as a form
    if request.method == 'POST':
      filename = images.save(form.image.data) #save the book image to the book_images directory in static
      return add_the_stock(request.form['isbn'],request.form['bkname'], request.form['author'],request.form['date'],request.form['desc'],filename,request.form.get("trade_price"),request.form.get("retail_price"),request.form.get("quantity"));
    else:
      return show_the_add_form();
  else:
    return redirect(url_for('index'));
  
  
def show_the_add_form():
  form = AddForm() #instatiates the AddForm class as a form
  if form.validate_on_submit(): #check if its a POST request
    print('Added succesfully');
  return render_template('add_stock.html',form=form)

def add_the_stock(isbn, book, author, date, desc,img,trade,retail,quantity): #this functions adds the books details to the database
  con = sqlite3.connect('book_stock.db')
  #check if databse exists, if doesn't create one
  try:
    con.execute('CREATE TABLE books (isbn INT PRIMARY KEY,bookname TEXT, author TEXT, date TEXT, description TEXT, image TEXT, trade_price INT, retail_price INT, quantity INT)')
    print('Table created successfully');
  except:
    pass
  con.close();
  
  #add the book details into the database
  con = sqlite3.connect('book_stock.db')
  image = 'static/images/book_images/' + img
  cur=con.execute('SELECT isbn FROM books') #select the isbn column
  done=False
  #create a list of isbn of books and check if the isbn of the book being added is in it already, if yes, update the trade price, retail price and quantity 
  isbn_list = [row for row, in cur]
  if int(isbn) in isbn_list:
    done=True
    con.execute('UPDATE books SET trade_price=?, retail_price=?,quantity=quantity+? WHERE isbn=?',(trade,retail,quantity,isbn))
  else:
    con.execute('INSERT INTO books values(?,?,?,?,?,?,?,?,?);', (isbn,book,author,date,desc,image,trade,retail,quantity))
  con.commit();
  con.close();
  
  return redirect('/stock_level');


  
  
