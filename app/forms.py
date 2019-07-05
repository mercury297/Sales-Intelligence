from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,DateField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,URL
from app.models import User,Data

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
    Company = StringField('Company', validators= [DataRequired])
    Industry = StringField('Industry')
    News_Date_from = DateField('News Date From', format='%m/%d/%Y')
    News_Date_to = DateField('News Date To', format='%m/%d/%Y')
    Mapped_to = StringField('Mapped to')
    submit = SubmitField('submit')

class CompanyFiltersForm(FlaskForm):
    Company = StringField('Company')
    Industry = StringField('Industry')
    News_Date_from = DateField('News Date From', format='%m/%d/%Y')
    News_Date_to = DateField('News Date To', format='%m/%d/%Y')
    Mapped_to = StringField('Mapped to')
    submit = SubmitField('submit')