from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

from backend.config import Config
from backend.models import User, Role
from backend.forms import CustomRegisterForm
from backend.database import db

app = Flask(__name__, template_folder='templates')
app.app_context().push()
app.config.from_object(Config)

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=CustomRegisterForm, register_form=CustomRegisterForm)