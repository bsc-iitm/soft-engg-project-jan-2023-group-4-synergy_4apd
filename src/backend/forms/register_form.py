from flask_security import RegisterForm
from wtforms import StringField, validators


class CustomRegisterForm(RegisterForm):
    name = StringField('Name', [validators.DataRequired('Name is required')])
    designation = StringField('Designation')
    
    bio = StringField('Bio')
    phone = StringField('Phone')
