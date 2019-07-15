from flask import render_template, flash, redirect,url_for,session,request
from app import app,db
from app.forms import LoginForm,RegistrationForm,ContactDataForm,CompanyDataForm,CompanyFiltersForm
from flask_login import current_user, login_user,logout_user
from app.models import User, Data, CompanyData
from flask_login import login_required
from werkzeug.urls import url_parse
from sqlalchemy import text
from werkzeug import secure_filename
import os,datetime
import pandas as pd
# from app.forms import 

#CUSTOMER.__table__.columns.keys() --> get list of column names

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/app/uploads'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
@app.route('/index')
@login_required
def index():
    return redirect(url_for('Company_Details'))  


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Company_Details'))
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
            next_page = url_for('Company_Details')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.pop('username',None)
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




@app.route('/Company_Details',methods = ['POST','GET'])
def Company_Details():
    if(current_user.is_authenticated):
        table = CompanyData.query.all()
        industries = []
        for val in table:
            industries.append(val.Industry)
        industries = list(set(industries))
        
        # print(industries)

        # print(request.form.get("industry"))
        form = CompanyFiltersForm()
        # form.showind()
        if form.is_submitted():    
            Company = form.Company.data
            # print(form.Industry.choices)
            Industry = form.Industry.data 
            News_Date_from = form.News_Date_from.data
            News_Date_to = form.News_Date_to.data
            Mapped_to = form.Mapped_to.data
            # a = [Company,Industry,News_Date_from,News_Date_to,Mapped_to]
            # print(a)
            # return a[1]

            stm = "select * from company_data "
            where = "where "
            first_flag = False
            if(Company):
                stm = stm + where + "Company =" + "\"" + Company + "\""
                first_flag = True    
            
            if(Industry):
                if(first_flag):
                    stm += " and " + " Industry = " + "\"" + Industry + "\"" 
                else:
                    stm = stm + where + " Industry =" + "\"" + Industry + "\""

            if(News_Date_from):
                if(first_flag):
                    stm += " and " + "News_Date_from =" + "\"" + News_Date_from + "\"" 
                else:
                    stm = stm + where + "News_Date_from =" + "\"" + News_Date_from + "\""

            if(News_Date_to):
                if(first_flag):
                    stm += " and " + "News_Date_to =" + "\"" + News_Date_to + "\"" 
                else:
                    stm = stm + where + "News_Date_to =" + "\"" + News_Date_to + "\""            
            
            if( Mapped_to):
                if(first_flag):
                    stm += " and " + " Mapped_to =" + "\"" +  Mapped_to + "\"" 
                else:
                    stm = stm + where + " Mapped_to =" + "\"" +  Mapped_to + "\""
            
            # print(stm)
            # return 'hi'
            stm = text(stm)
            table = CompanyData.query.from_statement(stm).all()
            # table = CompanyData.query.filter_by(Company = Company,Industry = Industry,News_Date_from = News_Date_from,News_Date_to = News_Date_to)
            # ,Industry = Industry,News_Date_from = News_Date_from
            # ,News_Date_to = News_Date_to, Mapped_to = Mapped_to)

            print(table)

            header = list(CompanyData.__table__.columns.keys())
            # print(form.Company.data)
            
            return render_template('company.html',table = table,header = header,form = form,industries = industries)
        # else:
        # table = CompanyData.query.all()
        # industries = []
        # for val in table:
        #     industries.append(val.Industry)
        # industries = list(set(industries))
        
        print(industries)
        header = list(CompanyData.__table__.columns.keys())
        
        # print(header,industries)

        return render_template('company.html',  table = table,header = header,industries = industries,form = form)
    else:
        return redirect(url_for('login'))

@app.route('/Contact_Details',methods = ['POST','GET'])
def Contact_Details():
    table = Data.query.all()
    header = list(Data.__table__.columns.keys())
    return render_template('contact.html', table = table,header = header)

# @app.route('/upload')
# def upload_file():
#    return render_template('uploads.html')
	
@app.route('/Company/uploader', methods = ['GET', 'POST'])
def upload_file():
   if current_user.is_authenticated:
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_excel(f)
        data_xls_dict = data_xls.to_dict()
        keys = list(data_xls_dict.keys())
        #   print(data_xls_dict[keys[0]][0])
        #   return 'no'
        #   print(data_xls.Company)
        company_obj = data_xls_dict[keys[0]]
        industry_obj = data_xls_dict[keys[1]]
        news_Date_from_obj = data_xls_dict[keys[2]]
        news_Date_to_obj = data_xls_dict[keys[3]]
        mapped_to_obj = data_xls_dict[keys[4]]
        #   temp = news_Date_from_obj[0].date()
        #   temp = datetime.datetime.strptime(str(temp), '%Y-%M-%d')
        #   temp = temp.strftime('%m/%d/%Y')

        #   print(str(temp))

        for row in range(len(company_obj)):
            temp1 , temp2 = str(news_Date_from_obj[row].date()),str(news_Date_from_obj[row].date())

            company = CompanyData(Company = company_obj[row],Industry = industry_obj[row]
            ,News_Date_from = temp1,News_Date_to = temp2,Mapped_to = mapped_to_obj[row])
            print(company)
            db.session.add(company)
            db.session.commit()

        #   print(data_xls['Contact Record Type'][0])


        return redirect(url_for('upload_file'))
    return render_template('uploads.html') 
   else:
       return redirect(url_for('login'))
