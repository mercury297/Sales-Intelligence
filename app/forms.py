from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,DateField,SelectField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,URL
from app.models import User,Data,CompanyData

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')    

class ContactDataForm(FlaskForm):
    Contact_Record_Type =  StringField('Contact_Record_Type')
    Created_Date = DateField('Created Date', format='%m/%d/%Y')
    Contact_ID = StringField('Contact_ID')
    Contact_Owner = StringField('Contact_Owner')
    First_Name = StringField('First_Name')
    Last_Name = StringField('Last_Name')
    Title = StringField('Title')
    Account_Name = StringField('Account Name')
    Industry = StringField('Industry')
    Email1 = StringField('Email1', validators=[DataRequired(), Email()])
    Email2 = StringField('Email2', validators=[Email()])
    #added later
    Phone = IntegerField('Phone')
    Linkedin_URL = StringField('Linkedin_URL',validators = [URL()])
    Contact_Status = StringField('Contact_Status')
    New_Lead_Source = StringField('New_Lead_Source')
    Services = StringField('Services')
    Products = StringField('Products')
    Mailing_City = StringField('Mailing_City')
    Mailing_State = StringField('Mailing_State')
    Mailing_Country = StringField('Mailing_Country')
    Account_Name = StringField('Account_Name')
    Region = StringField('Region')
    Campaigns_targetted = StringField('Campaigns_targetted')
    Email_Valid = StringField('Email_Valid')
    Last_Targetted = StringField('Last_Targetted')
    submit = SubmitField('Insert')


class CompanyDataForm(FlaskForm):
    Company = StringField('Company', validators= [DataRequired()])
    Industry = StringField('Industry') #SelectField('Industry')
    News_Date_from = DateField('News Date From', format='%Y-%m-%d')
    News_Date_to = DateField('News Date To', format='%Y-%m-%d')
    Mapped_to = StringField('Mapped to')
    submit = SubmitField('submit')

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

    choice_list = []
    for i in field_list:
        choice_list.append((i,i))
    field_list = list(filter(None, field_list)) 
    return choice_list

class CompanyFiltersForm(FlaskForm):
    Company = StringField('Company')
    table = CompanyData.query.all()

    industries = get_unique(table,'Industry' )
    
    Industry = SelectField('Industry',choices=industries)
    News_Date_from = StringField('News Date From') #DateField('News Date From', format='%m/%d/%Y')
    News_Date_to = StringField('News Date To') #DateField('News Date To', format='%m/%d/%Y')
    Mapped_to = StringField('Mapped to')
    submit = SubmitField('submit')

class ContactFiltersForm(FlaskForm):
    #lists for dropdowns
    table = Data.query.all()
    industries = get_unique(table,'Industry')
    status = get_unique(table,'Contact_Status')
    sources = get_unique(table,'New_Lead_Source')
    services = get_unique(table,'Services')
    products = get_unique(table,'Products')
    email_Valid = get_unique(table,'Email_Valid')
    
    #fields 
    Contact_Record_Type =  StringField('Contact_Record_Type')
    Created_Date = StringField('Created Date')
    Contact_ID = StringField('Contact_ID')
    Contact_Owner = StringField('Contact_Owner')
    First_Name = StringField('First_Name')
    Last_Name = StringField('Last_Name')
    Title = StringField('Title')
    Account_Name = StringField('Account Name')
    Industry = SelectField('Industry',choices= industries)
    Email1 = StringField('Email1', validators=[Email()])
    Email2 = StringField('Email2', validators=[Email()])
    #added later
    Linkedin_URL = StringField('Linkedin_URL',validators = [URL()])
    Contact_Status = SelectField('Contact_Status',choices = status)
    New_Lead_Source = SelectField('New_Lead_Source',choices = sources)
    Services = SelectField('Services',choices = services)
    Products = SelectField('Products',choices = products)
    Mailing_City = StringField('Mailing_City')
    Mailing_State = StringField('Mailing_State')
    Mailing_Country = StringField('Mailing_Country')
    Account_Name = StringField('Account_Name')
    Region = StringField('Region')
    Campaigns_targetted = StringField('Campaigns_targetted')
    Email_Valid = SelectField('Email_Valid',choices = email_Valid)
    Last_Targetted = StringField('Last_Targetted')
    submit = SubmitField('Apply')

