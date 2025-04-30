from flask import Flask, render_template, session, url_for, redirect, g
from pathlib import Path
from register_login import register_login
from stock import stock
from shopping import shopping
from checkout import checkout
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads, IMAGES, UploadSet
import sqlite3

#this is the driver file which runs all python files
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/';
app.config['UPLOADED_IMAGES_DEST'] = 'static/images/book_images' #sets the destination of the uploaded book image from add_stock
images = UploadSet('images', IMAGES) #specifies the type of  files to be uploads
configure_uploads(app, images)
app.register_blueprint(register_login, url_prefix="") #this registers the register_login python file
app.register_blueprint(stock, url_prefix="") #this registers the stock python file
app.register_blueprint(shopping,url_prefix="") #this registers the shopping python file
app.register_blueprint(checkout,url_prefix="") #this registers the checkout python file

Bootstrap(app)

#REFERENCE AULA MATERIALS
@app.before_request
#this function stores the username from the session cookie in 'g' before any request
def user_logged_in():
    user_id = session.get('username')
    user_pwd = session.get('password')
    if user_id is None:
        g.user = None;
    else:
        g.user = 'set';

#this function checks if a user has already been logged in, if not redirect to login
def login_required(view):
    @functools.wrap(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('register_login.login'));
        return view(**kwargs);
    return wrapped_view;

@app.route('/')
#this function is the starting directory of the website.
#it checks if a user is logged in a session an returns bookshop or login if not logged in
def index():
  if 'username' in session:
    if Path("book_stock.db").exists(): # this checks if the book stock database exists
      try:
        con = sqlite3.connect('book_stock.db')
        cursor = con.cursor();
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        return render_template('home.html', books=rows, Path=Path)
      except Exception as e:
        print(e);
      finally:
        cursor.close()
        con.close()    
    else:
      return render_template('home.html', Path=Path);
  else:
      return redirect(url_for('register_login.login'));


if __name__ == "__main__":
  app.run()
