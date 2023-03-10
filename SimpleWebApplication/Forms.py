from wtforms import Form, TextAreaField, validators, IntegerField, StringField, DateTimeField, SelectField, EmailField
from datetime import date, datetime
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, IntegerField
from wtforms.fields import EmailField, PasswordField

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
    if (int(field.data[0:2]) < month and int(field.data[2:]) <= year) or int(field.data[2:]) < year or int(
            field.data[0:2]) > 12:
        raise ValidationError('Card has expired')


def chk_alpha(form, field):
    new = field.data.replace(' ', '')  # .isalpha flags whitespaces
    if not new.isalpha():
        raise ValidationError("Names should not include numbers.")


def chk_date(form, field):
    if field.data.month > curr_month or field.data.year > curr_year:
        raise ValidationError("Date is pass today's date")


class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Customer Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=5, max=150), validators.DataRequired()])
    phone = IntegerField('Customer Telephone', [validators.Length(min=1, max=8), validators.Optional()])
    password = PasswordField('Password', [validators.Length(min=8, max=16), validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=16), validators.DataRequired()])


class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=16), validators.DataRequired()])


class ResetRequestForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])



class CartItem(Form):
    quantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=1, max=20)])
    remarks = TextAreaField('Special request(s)', [validators.Optional()])


class PayInfo(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=30)])
    address = StringField('Address', [validators.DataRequired(), validators.Length(min=1, max=40)])
    card = StringField('Credit Card Information',
                       [validators.DataRequired(), validators.Length(min=16, max=19), check_dat])
    exp = StringField("Expiry Date (MM/YY)", [validators.DataRequired(), validators.Length(min=4, max=4), date_chk])
    cvc = StringField("CVC", [validators.DataRequired(), validators.Length(min=3, max=3), check_dat])


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


class CreateFaqForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.DataRequired()])
