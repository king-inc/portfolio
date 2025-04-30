from flask import Flask, flash,url_for, request, redirect,make_response
from flask import session, Blueprint, render_template, g, abort
from markupsafe import escape
from flask_wtf import Form
from wtforms import StringField, PasswordField,DateField, TextAreaField,IntegerField,FileField
from wtforms.validators import InputRequired, length
import functools
import sqlite3


register_login = Blueprint("register_login",__name__) #this identifies this file as an add-on to driver file

#LoginForm class uses WTForms to create a form for login in
class LoginForm(Form):
    uname = StringField('Username', validators=[InputRequired()])
    pwd = PasswordField('Password', validators=[InputRequired()])

@register_login.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST': 
        return do_the_registration(request.form['uname'], request.form['pwd']);
    else:
        return show_the_registration_form(); #shows the registration form
    
def show_the_registration_form():
    form = LoginForm() #instatiates the LoginForm class as the form
    if form.validate_on_submit(): #check if details submitted have value in the input boxes
        print('Registered succesfully')
    return render_template('register.html', page=url_for('register_login.register'), form=form)

def do_the_registration(u,p): #add the new users to the database
    con = sqlite3.connect('registered_users.db')
    #check if database exists, if it doesn't create one
    try:
        con.execute('CREATE TABLE users (uname TEXT, pwd TEXT)')
        print('Table created successfully');
    except:
        pass
    con.close();
    
    #registers the users username and password into database
    con = sqlite3.connect('registered_users.db')
    con.execute("INSERT INTO users values(?,?);", (u,p))
    con.commit();
    con.close();
    
    return show_the_login_form(None)
    
    

@register_login.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        return do_the_login(request.form['uname'], request.form['pwd']);
    else:
        return show_the_login_form(None);
def show_the_login_form(error):
    form = LoginForm() #instatiates the LoginForm class as the form
    if form.validate_on_submit(): #check if login details submitted have value in the input boxes
        print('Logged in succesfully')
    return render_template('login.html', page=url_for('register_login.login'), form=form, error=error);

def do_the_login(u,p): 
    #check if user exists in database
    con = sqlite3.connect('registered_users.db');
    cur = con.cursor();
    cur.execute("SELECT count(*) FROM users WHERE uname=? AND pwd=?;",(u,p))
    if(int(cur.fetchone()[0]))>0:
        # set sessions ids
        session['username'] = u;
        session['password'] = p;
        return redirect(url_for('index'));
    else:
        error = "Invalid credentials. Please try again."
        return show_the_login_form(error);
        
@register_login.route('/logout') 
def logout(): #removes user from the session
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('index'))

  




  

    
