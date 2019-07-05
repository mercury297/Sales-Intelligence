from flask import render_template, flash, redirect,url_for,session,request
from app import app,db
from app.forms import LoginForm,RegistrationForm,ContactDataForm,CompanyDataForm,CompanyFiltersForm
from flask_login import current_user, login_user,logout_user
from app.models import User, Data, CompanyData
from flask_login import login_required
from werkzeug.urls import url_parse
# from app.forms import 

#CUSTOMER.__table__.columns.keys() --> get list of column names

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
        session['username'] = user.username
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    keys = session.keys()
    if('username' in keys and session['username'] == 'admin'):
        # if current_user.is_authenticated:
        #     return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)
    else:
        return 'not allowed'

@app.route('/admin/ContactData',methods = ['GET','POST'])
def ContactData():
    form = ContactDataForm()
    keys = session.keys()
    if('username' in keys and session['username'] == 'admin'):
        if form.validate_on_submit():
        # return 'inside'
        # return redirect(url_for('test')) 
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
            Phone = form.Phone.data
            Linkedin_URL = form.Linkedin_URL.data
            Contact_Status = form.Contact_Status.data
            New_Lead_Source = form.New_Lead_Source.data
            Services = form.Services.data
            Products = form.Products.data
            Mailing_City = form.Mailing_City.data
            Mailing_State = form.Mailing_State.data
            Mailing_Country = form.Mailing_Country.data
            Region = form.Region.data
            Campaigns_targetted = form.Campaigns_targetted.data
            Email_Valid = form.Email_Valid.data
            Last_Targetted = form.Last_Targetted.data
            data = Data( Contact_Record_Type =  Contact_Record_Type,Created_Date = Created_Date,Contact_ID = Contact_ID,Contact_Owner = Contact_Owner,First_Name = First_Name,Last_Name = Last_Name
            ,Title = Title,Account_Name = Account_Name,Industry = Industry,Email1 = Email1,Email2 = Email2,Phone = Phone,Linkedin_URL = Linkedin_URL,Contact_Status = Contact_Status 
            ,New_Lead_Source = New_Lead_Source,Services = Services,Products = Products,Mailing_City = Mailing_City,Mailing_State = Mailing_State,Mailing_Country = Mailing_Country
            ,Region = Region,Campaigns_targetted = Campaigns_targetted, Email_Valid = Email_Valid,Last_Targetted = Last_Targetted)
            db.session.add(data)
            db.session.commit()
            flash('Congratulations, entry added!')
            return redirect(url_for('index'))
    # return redirect(url_for('admin'))
        # return 'inside now 1'

        return render_template('ContactData.html', title='ContactData', form=form)    
    else:
        return 'not admin'

@app.route('/admin/CompanyData',methods = ['GET','POST'])
def company():
    form = CompanyDataForm()
    keys = session.keys()
    if('username' in keys and session['username'] == 'admin'):
        if form.validate_on_submit():
            Company = form.Company.data
            Industry = form.Industry.data
            News_Date_from = form.News_Date_from.data
            News_Date_to = form.News_Date_to.data
            Mapped_to = form.Mapped_to.data
            data = CompanyData(Company = Company,Industry = Industry,News_Date_from = News_Date_from,News_Date_to = News_Date_to,Mapped_to = Mapped_to)
            db.session.add(data)
            db.session.commit()
        return render_template('CompanyData.html', title='CompanyData', form=form)    
    else:
        return 'not admin'    


@app.route('/splash_page')
def splash_page():
    return render_template('home.html',title = 'Home')

@app.route('/Company_Details',methods = ['POST','GET'])
def Company_Details():
    form = CompanyFiltersForm()
    if form.is_submitted():
        Company = form.Company.data
        Industry = form.Industry.data
        News_Date_from = form.News_Date_from.data
        News_Date_to = form.News_Date_to.data
        Mapped_to = form.Mapped_to.data
        table = CompanyData.query.filter_by(Company = Company,Industry = Industry,News_Date_from = News_Date_from
        ,News_Date_to = News_Date_to, Mapped_to = Mapped_to)
        header = list(CompanyData.__table__.columns.keys())
        
        industries = []
        for val in table:
            industries.append(val.Industry)
        industries = list(set(industries))

        return render_template('company.html',table = table,header = header,form = form,industries = industries)
    # else:
    table = CompanyData.query.all()
    header = list(CompanyData.__table__.columns.keys())
    
    industries = []
    for val in table:
        industries.append(val.Industry)

    industries = list(set(industries))

    return render_template('company.html',  table = table,header = header,industries = industries,form = form)


@app.route('/Contact_Details',methods = ['POST','GET'])
def Contact_Details():
    details = Data.query.all()
    header = list(Data.__table__.columns.keys())
    return render_template('contact.html', table = table,header = header)
