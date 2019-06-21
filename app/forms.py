from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from app.models import User

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

class Admin(FlaskForm):
    Contact_Record_Type =  StringField('Contact Record Type')
    Created_Date = StringField('Created Date') #DateField('Created Date', format='%m/%d/%Y')
    Contact_ID = StringField('Contact ID')
    Contact_Owner = StringField('Contact Owner')
    First_Name = StringField('First Name')
    Last_Name = StringField('Last Name')
    Title = StringField('Title')
    Account_Name = StringField('Account Name')
    Industry = StringField('Industry')
    Email1 = StringField('Email1', validators=[DataRequired(), Email()])
    Email2 = StringField('Email2', validators=[Email()])
    submit = SubmitField('Insert')
    #for later
    # Phone = 
    # Linkedin_URL = 
    # Contact_Status = 
    # New_Lead_Source = 
    # Services = 
    # Products = 
    # Mailing_City = 
    # Mailing_State = 
    # Mailing_Country = 
    # Account_Name = 
    # Region = 
    # Campaigns_targetted = 
    # Email_Valid = 
    # Last_Targetted = 