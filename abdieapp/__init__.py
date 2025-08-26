#first open init beside the template folder which is the top root init. 
# after the init inside the template next is config.py not in instance
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

#instantiate an object of Flask app
app = Flask(__name__, instance_relative_config=True)

#loading CSRF
csrf=CSRFProtect(app)

#Load the config file
from abdieapp import config

app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py', silent=False) #this is the config in instance folders

#database connection
db=SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)

#load your routes here
from abdieapp.myroutes import routes #since routes is now a module on its own

#load models
from abdieapp import models