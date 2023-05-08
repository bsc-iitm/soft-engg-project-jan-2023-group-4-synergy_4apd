from wtforms import Form
from wtforms import StringField, TextAreaField, validators

class ProfileForm(Form):
    name = StringField('Name', [validators.DataRequired('Name is required')])
    designation = StringField('Designation')
    bio = TextAreaField('Bio')
    phone = StringField('Phone')