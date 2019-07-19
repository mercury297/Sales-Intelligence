from flask import render_template, flash, redirect,url_for,session,request
from app import app,db
from app.forms import LoginForm,RegistrationForm,ContactDataForm,CompanyDataForm,CompanyFiltersForm,ContactFiltersForm
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

#function to create company filter string
def company_filter_string(Company,Industry,News_Date_from,News_Date_to,Mapped_to):
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
    
    return stm

def get_unique(table,field):
    field_list = []
    if(field == 'Industry'):
        for val in table:
            field_list.append(val.Industry)
        field_list = list(set(field_list))
    elif(field == 'Contact_Status'):
        for val in table:
            field_list.append(val.Contact_Status)
        field_list = list(set(field_list))
    elif(field == 'New_Lead_Source'):
        for val in table:
            field_list.append(val.New_Lead_Source)
        field_list = list(set(field_list))
    elif(field == 'Services'):
        for val in table:
            field_list.append(val.Services)
        field_list = list(set(field_list))
    elif(field == 'Products'):
        for val in table:
            field_list.append(val.Products)
        field_list = list(set(field_list))    
    elif(field == 'Email_Valid'):
        for val in table:
            field_list.append(val.Email_Valid)
        field_list = list(set(field_list))    
    field_list = list(filter(None, field_list)) 
    return field_list

@app.route('/Company_Details',methods = ['POST','GET'])
def Company_Details():
    if(current_user.is_authenticated):
        table = CompanyData.query.all()
        industries = get_unique(table,'Industry')
        form = CompanyFiltersForm()

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
            stm = company_filter_string(Company,Industry,News_Date_from,News_Date_to,Mapped_to)    
    
            stm = text(stm)
            table = CompanyData.query.from_statement(stm).all()
            # table = CompanyData.query.filter_by(Company = Company,Industry = Industry,News_Date_from = News_Date_from,News_Date_to = News_Date_to)
            # ,Industry = Industry,News_Date_from = News_Date_from
            # ,News_Date_to = News_Date_to, Mapped_to = Mapped_to)

            # print(table)

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
        header.remove('company_id')
        # print(header,industries)

        return render_template('company.html',  table = table,header = header,industries = industries,form = form)
    else:
        return redirect(url_for('login'))


def contact_filter_string(Contact_Record_Type,Created_Date,Contact_ID 
                        ,Contact_Owner,First_Name ,Last_Name
                        ,Title ,Account_Name,Industry
                        ,Email1 ,Email2 ,Linkedin_URL,Contact_Status
                        ,New_Lead_Source,Services,Products
                        ,Mailing_City ,Mailing_State,Mailing_Country
                        ,Region ,Campaigns_targetted,Email_Valid 
                        ,Last_Targetted):
        
                        stm = "select * from data "
                        where = "where "
                        first_flag = False
                        if(Contact_Record_Type):
                            stm = stm + where + "Contact_Record_Type =" + "\"" + Contact_Record_Type + "\""
                            first_flag = True
                        if(Created_Date):    
                            if(first_flag):
                                stm += " and " + " Created_Date = " + "\"" + Created_Date + "\"" 
                            else:
                                stm = stm + where + " Created_Date =" + "\"" + Created_Date + "\""
                        if(Contact_ID):
                            if(first_flag):
                                stm += " and " + " Contact_ID = " + "\"" + Contact_ID + "\"" 
                            else:
                                stm = stm + where + " Contact_ID =" + "\"" + Contact_ID + "\""
                        if(Contact_Owner):
                            if(first_flag):
                                stm += " and " + " Contact_Owner = " + "\"" + Contact_Owner + "\"" 
                            else:
                                stm = stm + where + " Contact_Owner =" + "\"" + Contact_Owner + "\""
                        if(First_Name):
                            if(first_flag):
                                stm += " and " + " First_Name = " + "\"" + First_Name + "\"" 
                            else:
                                stm = stm + where + " First_Name =" + "\"" + First_Name + "\""
                        if(Last_Name):
                            if(first_flag):
                                stm += " and " + " Last_Name = " + "\"" + Last_Name + "\"" 
                            else:
                                stm = stm + where + " Last_Name =" + "\"" + Last_Name + "\""
                        if(Title):
                            if(first_flag):
                                stm += " and " + " Title = " + "\"" + Title + "\"" 
                            else:
                                stm = stm + where + " Title =" + "\"" + Title + "\""
                        if(Account_Name):
                            if(first_flag):
                                stm += " and " + " Account_Name = " + "\"" + Account_Name + "\"" 
                            else:
                                stm = stm + where + " Account_Name =" + "\"" + Account_Name + "\""
                        if(Industry):
                            if(first_flag):
                                stm += " and " + " Industry = " + "\"" + Industry + "\"" 
                            else:
                                stm = stm + where + " Industry =" + "\"" + Industry + "\""
                        if(Email1):    
                            if(first_flag):
                                stm += " and " + " Email1 = " + "\"" + Email1 + "\"" 
                            else:
                                stm = stm + where + " Email1 =" + "\"" + Email1 + "\""
                        if(Email2):
                            if(first_flag):
                                stm += " and " + " Email2 = " + "\"" + Email2 + "\"" 
                            else:
                                stm = stm + where + " Email2 =" + "\"" + Email2 + "\""
                        if(Linkedin_URL):    
                            if(first_flag):
                                stm += " and " + " Linkedin_URL = " + "\"" + Linkedin_URL + "\"" 
                            else:
                                stm = stm + where + " Linkedin_URL =" + "\"" + Linkedin_URL + "\""
                        if(Contact_Status and Contact_Status!='None'):    
                            if(first_flag):
                                stm += " and " + " Contact_Status = " + "\"" + Contact_Status + "\"" 
                            else:
                                stm = stm + where + " Contact_Status =" + "\"" + Contact_Status + "\""
                        if(New_Lead_Source and New_Lead_Source!='None'):
                            if(first_flag):
                                stm += " and " + " New_Lead_Source = " + "\"" + New_Lead_Source + "\"" 
                            else:
                                stm = stm + where + " New_Lead_Source =" + "\"" + New_Lead_Source + "\""
                        if(Services and Services!= 'None'):    
                            if(first_flag):
                                stm += " and " + " Services = " + "\"" + Services + "\"" 
                            else:
                                stm = stm + where + " Services =" + "\"" + Services + "\""
                        if(Products and Products!= 'None'):    
                            if(first_flag):
                                stm += " and " + " Products = " + "\"" + Products + "\"" 
                            else:
                                stm = stm + where + " Products =" + "\"" + Products + "\""
                        if(Mailing_City ):    
                            if(first_flag):
                                stm += " and " + " Mailing_City = " + "\"" + Mailing_City + "\"" 
                            else:
                                stm = stm + where + " Mailing_City =" + "\"" + Mailing_City + "\""
                        if(Mailing_State):    
                            if(first_flag):
                                stm += " and " + " Mailing_State = " + "\"" + Mailing_State + "\"" 
                            else:
                                stm = stm + where + " Mailing_State =" + "\"" + Mailing_State + "\""
                        if(Mailing_Country):    
                            if(first_flag):
                                stm += " and " + " Mailing_Country = " + "\"" + Mailing_Country + "\"" 
                            else:
                                stm = stm + where + " Mailing_Country =" + "\"" + Mailing_Country + "\""
                        if(Region):    
                            if(first_flag):
                                stm += " and " + " Region = " + "\"" + Region + "\"" 
                            else:
                                stm = stm + where + " Region =" + "\"" + Region + "\""
                        if(Campaigns_targetted):
                            if(first_flag):
                                stm += " and " + " Campaigns_targetted = " + "\"" + Campaigns_targetted + "\"" 
                            else:
                                stm = stm + where + " Campaigns_targetted =" + "\"" + Campaigns_targetted + "\""
                        if(Email_Valid and Email_Valid !='None'):
                            if(first_flag):
                                stm += " and " + " Email_Valid = " + "\"" + Email_Valid + "\"" 
                            else:
                                stm = stm + where + " Email_Valid =" + "\"" + Email_Valid + "\""
                        if(Last_Targetted):    
                            if(first_flag):
                                stm += " and " + " Last_Targetted = " + "\"" + Last_Targetted + "\"" 
                            else:
                                stm = stm + where + " Last_Targetted =" + "\"" + Last_Targetted + "\""
                        
                        return stm


@app.route('/Contact_Details',methods = ['POST','GET'])
def Contact_Details():
    if current_user.is_authenticated:    
        table = Data.query.all()
        header = list(Data.__table__.columns.keys())
        industries = get_unique(table,'Industry')
        # titles = get_unique(table,'Title')
        status = get_unique(table,'Contact_Status')
        sources = get_unique(table,'New_Lead_Source')
        services = get_unique(table,'Services')
        products = get_unique(table,'Products')
        email_valid = get_unique(table,'Email_Valid')
        print(services)
        form = ContactFiltersForm()

        # return '1'
        if form.is_submitted():
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
 
            stm = contact_filter_string(Contact_Record_Type,Created_Date,Contact_ID 
                                        ,Contact_Owner,First_Name ,Last_Name
                                        ,Title ,Account_Name,Industry
                                        ,Email1 ,Email2 ,Linkedin_URL,Contact_Status
                                        ,New_Lead_Source,Services,Products
                                        ,Mailing_City ,Mailing_State,Mailing_Country
                                        ,Region ,Campaigns_targetted,Email_Valid 
                                        ,Last_Targetted )
            stm = text(stm)
            # return str(stm)
            table = Data.query.from_statement(stm).all()
            return render_template('contact.html', table = table,header = header,form = form
                            ,status = status,sources = sources,services = services,products = products,email_valid = email_valid)

    
        header = list(Data.__table__.columns.keys())
        return render_template('contact.html', table = table,header = header,form = form
                            ,status = status,sources = sources,services = services,products = products,email_valid = email_valid)
    else:
        return redirect(url_for('login'))
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
