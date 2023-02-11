from wtforms import Form, TextAreaField, validators, IntegerField, StringField, DateTimeField, SelectField, EmailField
from datetime import date, datetime
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
now = str(date.today())
year = int(now[2:4])
month = int(now[5:7])

curr = datetime.now()
curr_month = curr.month
curr_year = curr.year

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

def chk_alpha(form, field):
    if not field.data.isalpha():
        raise ValidationError("Names should not include numbers.")

def chk_date(form, field):
    if field.data.month > curr_month or field.data.year > curr_year:
        raise ValidationError("Date is pass today's date")

class CartItem(Form):
    quantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=1, max=20)])
    remarks = TextAreaField('Special request(s)', [validators.Optional()])

class PayInfo(Form):
    name = StringField('Name',[validators.DataRequired(), validators.Length(min=1, max=30)])
    address = StringField('Address',[validators.DataRequired(), validators.Length(min=1, max=40)])
    card = StringField('Credit Card Information',[validators.DataRequired(), validators.Length(min=16, max=19),check_dat])
    exp = StringField("Expiry Date (MM/YY)",[validators.DataRequired(),validators.Length(min=4,max=4),date_chk])
    cvc = StringField("CVC",[validators.DataRequired(),validators.Length(min=3,max=3),check_dat])

class CreateOrderForm(FlaskForm):
    class Meta:
        csrf = False

    date = DateTimeField('Time', format="%d/%m/%Y %H:%M:%S", default=datetime.now,
                         validators=[validators.DataRequired(), chk_date])
    restaurant_name = StringField('Restaurant Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    no_of_items = IntegerField('Number of Items', [validators.DataRequired()])
    area = SelectField('Area', [validators.DataRequired()],
                       choices=[('', 'Select'), ('Central', 'Central'), ('East', 'East'), ('North', 'North'),
                                ('North-East', 'North-East'), ('West', 'West')])
    driver_name = StringField("Driver's name",
                              [validators.Length(min=1, max=150), validators.DataRequired(), chk_alpha])
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CreateDriverForm(FlaskForm):
    class Meta:
        csrf = False

    driver_name = StringField("Driver's name", [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
                         default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    area = StringField('Area', [validators.Length(min=1, max=150), validators.DataRequired()])
    no_of_items = IntegerField('Number of Items', [validators.DataRequired()])
    address = StringField('Address', [validators.length(max=200), validators.DataRequired()])
    vehicle = SelectField('Delivery Vehicle', [validators.DataRequired()],
                          choices=[('', 'Select'), ('Bicycle', 'Bicycle'), ('PMD', 'Personal Mobility Device'),
                                   ('On Foot', 'On Foot')],
                          default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])