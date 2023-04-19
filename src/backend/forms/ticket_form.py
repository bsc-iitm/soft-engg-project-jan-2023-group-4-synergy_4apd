from wtforms import Form, StringField, TextAreaField, BooleanField
from wtforms import validators


class TicketForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(max=50)])

    message = TextAreaField('Message', [validators.DataRequired()])

    is_public = BooleanField('Publicly visible?')
