from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import os


#app instance
app = Flask(__name__)
app.config.from_object(Config)
#file upload config
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#db instance
db =  SQLAlchemy(app)
migrate = Migrate(app,db)

#login manager instance
login = LoginManager(app)
# login_manager.init_app(app)
login.login_view = 'login'

#routes has the page routes
#models has db models
from app import routes,models

#mail instance
mail = Mail(app)
