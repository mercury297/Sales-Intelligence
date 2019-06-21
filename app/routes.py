from flask import render_template, flash, redirect,url_for
from app import app,db
from app.forms import LoginForm
from flask_login import current_user, login_user,logout_user
from app.models import User
from flask_login import login_required
from app.forms import RegistrationForm,Admin

@app.route('/')
@app.route('/index')
@login_required
def index():
    return 'yet to happen'  

@app.route('/test')
def display():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('test.html', user=user,posts= posts,title="title")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if(user.username == 'admin'):
              return redirect(url_for('admin'))
        elif user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin',methods = ['GET','POST'])
def admin():
    form = Admin()
    if(form.validate_on_submit()):    
        Contact_Record_Type = form.Contact_Record_Type.data
        Created_Date = form.Created_Date.data
        Contact_ID = form.Contact_ID.data
        Contact_Owner = form.Contact_Owner.data
        First_Name = form.First_Name.data
        Last_Name = form.Last_Name.data
        Title = form.Title.data
        Account_Name = form.Account_Name.data
        Industry = form.Industry.data
        Email1 = form.Email1.data
        Email2 = form.Email2.data
        data = Data( Contact_Record_Type =  Contact_Record_Type,Created_Date = Created_Date,Contact_ID = Contact_ID,Contact_Owner = Contact_Owner,First_Name = First_Name,Last_Name = First_Name
        ,Title = Title,Account_Name = Account_Name,Industry = Industry,Email1 = Email1,Email2 = Email2)
        flash('Congratulations, you are now a registered user!')
        db.session.add(data)
        db.session.commit()
        flash('Congratulations, entry added!')
        return redirect(url_for('admin'))

    return render_template('admin.html', title='Admin', form=form)
        





