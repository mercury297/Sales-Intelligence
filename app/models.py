from app import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Data(db.Model):
    Contact_Record_Type = db.Column(db.String(64))
    Created_Date = db.Column(db.String(64))
    Contact_ID =  db.Column(db.String(64), primary_key=True)
    Contact_Owner = db.Column(db.String(64))
    First_Name = db.Column(db.String(64))
    Last_Name = db.Column(db.String(64))
    Title = db.Column(db.String(64))
    Account_Name = db.Column(db.String(64))
    Industry = db.Column(db.String(64))
    Email1 = db.Column(db.String(64))
    Email2 = db.Column(db.String(64))


    def __repr__(self):
        return '<Data {}>'.format(self.Contact_ID) 

#     Phone = db.Column(db.Integer(64))
#     Linkedin_URL = db.Column(db.String(64))
#     Contact_Status = db.Column(db.String(64))
#     New_Lead_Source = db.Column(db.String(64))
#     Services = db.Column(db.String(64))
#     Products = db.Column(db.String(64))
#     Mailing_City = db.Column(db.String(64))
#     Mailing_State = db.Column(db.String(64))
#     Mailing_Country = db.Column(db.String(64))
#     Account_Name = db.Column(db.String(64))
#     Region = db.Column(db.String(64))
#     Campaigns_targetted = db.Column(db.String(64))
#     Email_Valid = db.Column(db.String(64))
#     Last_Targetted = db.Column(db.String(64))
#     # 'Email Valid', 'Last Targetted'


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))        