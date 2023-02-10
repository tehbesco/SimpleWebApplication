from wtforms import Form, TextAreaField, validators, IntegerField, StringField
from datetime import date
from wtforms.validators import ValidationError
now = str(date.today())
year = int(now[2:4])
month = int(now[5:7])

def check_dat(form, field):
    for i in range(len(field.data)):
        if (field.data)[i].isalpha():
            raise ValidationError('Field must be integer')

def date_chk(form, field):
    for i in range(len(field.data)):
        if (field.data)[i].isalpha():
            raise ValidationError('Field must be integer')
    if (int(field.data[0:2]) < month and int(field.data[2:]) <= year) or int(field.data[2:]) < year or int(field.data[0:2]) > 12:
        raise ValidationError('Card has expired')

class CartItem(Form):
    quantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=1, max=20)])
    remarks = TextAreaField('Special request(s)', [validators.Optional()])

class PayInfo(Form):
    name = StringField('Name',[validators.DataRequired(), validators.Length(min=1, max=30)])
    address = StringField('Address',[validators.DataRequired(), validators.Length(min=1, max=40)])
    card = StringField('Credit Card Information',[validators.DataRequired(), validators.Length(min=16, max=19),check_dat])
    exp = StringField("Expiry Date (MM/YY)",[validators.DataRequired(),validators.Length(min=4,max=4),date_chk])
    cvc = StringField("CVC",[validators.DataRequired(),validators.Length(min=3,max=3),check_dat])


