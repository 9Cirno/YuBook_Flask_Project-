from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired,Regexp


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[
        DataRequired(),
        Length(min=2, max=29, message='The length of receiver\'s name in 2-20 characters ')
    ])

    mobile = StringField(validators=[
        DataRequired()
       # Regexp('^1[0-9]{10}$'), 0, 'please enter phone number in correct form')
    ])

    message = StringField()

    address = StringField(validators=[
        DataRequired(),
        Length(min=10,max=70,message='The length of receiver\'s address in 10-70 characters')
    ])
