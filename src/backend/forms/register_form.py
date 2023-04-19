from flask_security import RegisterForm
from wtforms import StringField, TextAreaField, validators


class CustomRegisterForm(RegisterForm):
    name = StringField('Name', [validators.DataRequired('Name is required')])
    designation = StringField('Designation')
    
    bio = TextAreaField('Bio')
    phone = StringField('Phone')
