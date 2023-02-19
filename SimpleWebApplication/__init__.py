from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask import *
import pandas as pd
import openpyxl
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, equal_to
from flask_bcrypt import Bcrypt
from flask_wtf import Form
from flask import Flask, request, redirect, url_for
from Forms import CreateCustomerForm, LoginForm, ResetRequestForm
import shelve
from flask import render_template
import secrets
import string
import smtplib
from datetime import date, datetime
from collections import Counter
from math import ceil
from Forms import CartItem, PayInfo, CreateOrderForm, CreateFaqForm
from classes import *
import shelve, os, Faq

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
basedata = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = sessionmaker(engine)()

metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

SEPARATOR = "++"


def get_data(table, column):
    sa_table = getattr(Base.classes, table)
    col = getattr(sa_table, column)
    rows = session.query(col).all()
    cnt = Counter()
    for row in rows:
        attr = row[0]

        if attr is None:
            continue

        if isinstance(attr, (date, datetime)):
            attr = attr.strftime("%Y-%m")

        cnt[attr] += 1
    return sorted(cnt.items())


def calculate_max_height_graph(values):
    max_value = max(values)
    return int(ceil(max_value / 100.0)) * 100


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)


class orderList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    area = db.Column(db.String(100), nullable=False)
    dri_name = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(100))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sub', methods=["GET", "POST"])
def sub():
    pay_info = PayInfo(request.form)
    if request.method == "POST" and pay_info.validate():
        data = dict(request.form)
        db = shelve.open('pay.db', 'w')
        count = len(db.keys())
        db[str(count + 1)] = data
        db.close()
        res = make_response(render_template("resub.html"))
        res.set_cookie("sub", "Y")
        return res
    return render_template('sub.html', form=pay_info)


@app.route('/resub')
def resub():
    return render_template('resub.html')


@app.route('/delete-cookie', methods=['GET', 'POST'])
def delete_cookie():
    res = make_response(render_template("home.html"))
    res.set_cookie('sub', 'Y', max_age=0)
    return res


@app.route('/foodSearch', methods=['GET', 'POST'])
def search():
    db = shelve.open("search.db", 'c')
    db.close()
    db = shelve.open("search.db", 'r')
    if "search" in db:
        search = db["search"]
        src = db["src"]
    else:
        db.clear()
        search = ""
        src = "name"
    db.close()
    if request.method == "POST":
        data = dict(request.form)
        if "submit-button" in data.keys():
            id = data["submit-button"]
            return redirect(url_for('create_cart', food_id=id))
        elif "search" in data.keys():
            src = data['btnradio']
            search = data["search"]
            db = shelve.open("search.db", 'c')
            db["search"] = search
            db["src"] = src
            db.close()
            page = 1
    else:
        page = request.args.get('page', 1, type=int)
    if src == "res":
        foods = Foods.query.filter(Foods.restaurant.like('%' + search + '%'))
    elif src == "tags":
        foods = Foods.query.filter(Foods.tags.like('%' + search + '%'))
    else:
        foods = Foods.query.filter(Foods.name.like('%' + search + '%'))
    pagination = foods.paginate(page=page, per_page=5)
    return render_template('foodSearch.html', pagination=pagination)


@app.route('/rewards')
def rewards():
    return render_template('rewards.html')


@app.route('/createCart', methods=['GET', 'POST'])
def create_cart():
    food_id = request.args["food_id"]
    food = Foods.query.get(food_id)
    name = food.name
    price = food.price
    restaurant = food.restaurant
    cart_item = CartItem(request.form)
    if request.method == 'POST' and cart_item.validate():
        items_dict = {}
        db = shelve.open('cart.db', 'c')

        try:
            items_dict = db['Items']
        except:
            print("Error in retrieving Items from cart.db.")
        cart = Cart(name, cart_item.quantity.data, cart_item.remarks.data, price)
        items_dict[cart.get_item_id()] = cart
        db['Items'] = items_dict
        db.close()
        return redirect(url_for('retrieve_cart'))
    return render_template('createCart.html', form=cart_item, name=name, res=restaurant, price=price)


@app.route('/retrieveCart')
def retrieve_cart():
    items_dict = {}
    db = shelve.open('cart.db', 'r')
    items_dict = db['Items']
    db.close()
    items_list = []
    for key in items_dict:
        item = items_dict.get(key)
        items_list.append(item)
    return render_template('retrieveCart.html', count=len(items_list), items_list=items_list)


@app.route('/updateCart/<int:id>/', methods=['GET', 'POST'])
def update_cart(id):
    update_cart_form = CartItem(request.form)
    if request.method == 'POST' and update_cart_form.validate():
        items_dict = {}
        db = shelve.open('cart.db', 'w')
        items_dict = db['Items']

        user = items_dict.get(id)
        user.set_quantity(update_cart_form.quantity.data)
        user.set_remarks(update_cart_form.remarks.data)

        db['Items'] = items_dict
        db.close()

        return redirect(url_for('retrieve_cart'))
    else:
        items_dict = {}
        db = shelve.open('cart.db', 'r')
        items_dict = db['Items']
        db.close()
        user = items_dict.get(id)
        update_cart_form.quantity.data = user.get_quantity()
        update_cart_form.remarks.data = user.get_remarks()

        return render_template('updateCart.html', form=update_cart_form)


@app.route('/deleteCart/<int:id>', methods=['POST'])
def delete_cart(id):
    items_dict = {}
    db = shelve.open('cart.db', 'w')
    items_dict = db['Items']

    items_dict.pop(id)

    db['Items'] = items_dict
    db.close()

    return redirect(url_for('retrieve_cart'))


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    items_dict = {}
    db = shelve.open('cart.db', 'r')
    items_dict = db['Items']
    db.close()
    items_list = []
    ttl = 0
    for key in items_dict:
        ttl += items_dict[key].get_cost() * items_dict[key].get_quantity()
        item = items_dict.get(key)
        items_list.append(item)
    pay_info = PayInfo(request.form)
    if request.cookies.get("sub") == "Y":
        discount = 15
    else:
        discount = 0
    if request.method == 'POST' and pay_info.validate():
        data = dict(request.form)
        db = shelve.open('pay.db', 'w')
        count = len(db.keys())
        db[str(count + 1)] = data
        db.close()
        return redirect(url_for('track'))
    return render_template('pay.html', form=pay_info, items_list=items_list, total=ttl, disc=discount)


@app.route('/track')
def track():
    return render_template('track.html')


# <-------------------------------------------------------------------------------------------->
# <------------------------------ Milhan's app.routes start here ------------------------------>
# <-------------------------------------------------------------------------------------------->

@app.route('/staff')
def staff_home():
    return render_template('staff_home.html')


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    orders_dict = {}
    create_order_form = CreateOrderForm(request.form)
    if request.method == 'POST' and create_order_form.validate():
        dbs = shelve.open('order.db', 'c')

        try:
            orders_dict = dbs['orders']
        except:
            print("Error in retrieving orders from order.db.")

        order = Order(create_order_form.date.data, create_order_form.restaurant_name.data,
                      create_order_form.no_of_items.data, create_order_form.area.data,
                      create_order_form.remarks.data, create_order_form.driver_name.data)

        order2 = orderList(date=create_order_form.date.data,
                           name=create_order_form.restaurant_name.data,
                           num=create_order_form.no_of_items.data,
                           area=create_order_form.area.data,
                           dri_name=create_order_form.driver_name.data,
                           remarks=create_order_form.remarks.data)

        orders_dict[order.get_order_id()] = order
        dbs['orders'] = orders_dict

        dbs.sync()
        dbs.close()

        db.session.add(order2)
        db.session.commit()

        rand = orderList.query.filter_by(dri_name="asd").all()
        print("rand value: ", rand)

        return redirect(url_for('retrieve_orders'))
    return render_template('createOrder.html', form=create_order_form)


@app.route('/retrieveOrders')
def retrieve_orders():
    orders_dict = {}
    dbs = shelve.open('order.db', 'r')

    orders_dict = dbs['orders']
    dbs.sync()
    dbs.close()
    print(orders_dict)

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    print(orders_list)
    print("all orderList entries: ", orderList.query.all())

    return render_template('retrieveOrders.html', count=len(orders_list), orders_list=orders_list)


@app.route('/visualiseOrders')
def visualise_orders():
    table = orderList.query.all()
    return render_template('visualiseOrders.html', table=table)


@app.route('/updateOrder/<int:id>/', methods=['GET', 'POST'])
def update_order(id):
    update_order_form = CreateOrderForm(request.form)
    if request.method == 'POST' and update_order_form.validate():
        orders_dict = {}
        dbs = shelve.open('order.db', 'w')
        orders_dict = dbs['orders']

        order = orders_dict.get(id)
        order.set_date(update_order_form.date.data)
        order.set_restaurant_name(update_order_form.restaurant_name.data)
        order.set_no_of_items(update_order_form.no_of_items.data)
        order.set_area(update_order_form.area.data)
        order.set_driver_name(update_order_form.driver_name.data)
        order.set_remarks(update_order_form.remarks.data)

        dbs['orders'] = orders_dict
        dbs.sync()
        dbs.close()

        entry = orderList.query.filter_by(id=id).first()
        print("entry: ", entry)

        entry.date = update_order_form.date.data
        entry.name = update_order_form.restaurant_name.data
        entry.num = update_order_form.no_of_items.data
        entry.area = update_order_form.area.data
        entry.dri_name = update_order_form.driver_name.data
        entry.remarks = update_order_form.remarks.data

        db.session.commit()

        return redirect(url_for('retrieve_orders'))
    else:
        orders_dict = {}
        dbs = shelve.open('order.db', 'r')
        orders_dict = dbs['orders']
        dbs.sync()
        dbs.close()

        order = orders_dict.get(id)
        update_order_form.date.data = order.get_date()
        update_order_form.restaurant_name.data = order.get_restaurant_name()
        update_order_form.no_of_items.data = order.get_no_of_items()
        update_order_form.area.data = order.get_area()
        update_order_form.driver_name.data = order.get_driver_name()
        update_order_form.remarks.data = order.get_remarks()

        return render_template('updateOrder.html', form=update_order_form)


@app.route('/deleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    orders_dict = {}
    dbs = shelve.open('order.db', 'w')
    orders_dict = dbs['orders']

    orders_dict.pop(id)

    dbs['orders'] = orders_dict
    dbs.sync()
    dbs.close()

    deli = orderList.query.filter_by(id=id).first()
    if deli is not None:
        db.session.delete(deli)
        db.session.commit()

    return redirect(url_for('retrieve_orders'))


# <------------------------------------------------------------------------------------>
# <------------------------------ Graph code starts here ------------------------------>
# <------------------------------------------------------------------------------------>


@app.route('/dataGraph')
def page():
    tables = sorted(Base.classes.keys())
    return render_template("dataGraph.html",
                           tables=tables)


@app.route('/columns')
def show_columns():
    table_str = request.args["table"]
    table = Base.classes.get(table_str)
    table_columns = {
        col: f"{table_str}{SEPARATOR}{col}" for col in
        table.__table__.columns.keys()
    }
    return render_template('includes/_columns.html',
                           table_columns=sorted(table_columns.items()))


@app.route('/graph')
def build_graph():
    tcolumn = request.args["tcolumn"]
    table, column = tcolumn.split(SEPARATOR)
    data = get_data(table, column)
    labels, values = zip(*data)
    max_height = calculate_max_height_graph(values)
    return render_template('includes/_graph.html',
                           labels=labels,
                           values=values,
                           max_height=max_height)


@app.route('/export', methods=['GET', 'POST'])
def export_data():
    data = orderList.query.all()
    data_list = [to_dict(item) for item in data]
    df = pd.DataFrame(data_list)

    filename = "restaurant_data.xlsx"
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name='Data')
    writer.close()

    return send_file(filename)


# <-------------------------------------------------------------------------------------------->
# <------------------------------ yangyus stuf------------------------------->

@app.route('/faq', methods=['GET', 'POST'])
def create_faq():
    create_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and create_faq_form.validate():
        faqs_dict = {}
        db = shelve.open('faq.db', 'c')

        try:
            faqs_dict = db['Faqs']
        except:
            print("Error in retrieving Faqs from faq.db")

        faq = Faq.Faq(create_faq_form.email.data, create_faq_form.remarks.data)
        faqs_dict[faq.get_faq_id()] = faq
        db['Faqs'] = faqs_dict

        faqs_dict = db['Faqs']
        faq = faqs_dict[faq.get_faq_id()]
        print(faq.get_email(), "was stored in faq.db successfully with faq_id ==",
              faq.get_faq_id())

        db.close()

        return redirect(url_for('home'))
    return render_template('faq.html', form=create_faq_form)


@app.route('/retrievefaq')
def retrieve_faq():
    faqs_dict = {}
    db = shelve.open('faq.db', 'r')
    faqs_dict = db['Faqs']
    db.close()

    faqs_list = []
    for key in faqs_dict:
        faq = faqs_dict.get(key)
        faqs_list.append(faq)

    return render_template('retrieveFaq.html', count=len(faqs_list), faqs_list=faqs_list)


@app.route('/updateFaq/<int:id>/', methods=['GET', 'POST'])
def update_faq(id):
    update_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and update_faq_form.validate():
        faqs_dict = {}
        db = shelve.open('faq.db', 'w')
        faqs_dict = db['Faqs']

        faq = faqs_dict.get(id)
        faq.set_email(update_faq_form.email.data)
        faq.set_remarks(update_faq_form.remarks.data)

        db['Faqs'] = faqs_dict
        db.close()
        return redirect(url_for('retrieve_faq'))
    else:
        faqs_dict = {}
        db = shelve.open('faq.db', 'r')
        faqs_dict = db['Faqs']
        db.close()
        faq = faqs_dict.get(id)
        update_faq_form.email.data = faq.get_email()
        update_faq_form.remarks.data = faq.get_remarks()
    return render_template('updateFaq.html', form=update_faq_form)


@app.route('/deleteFaq/<int:id>', methods=['POST'])
def delete_faq(id):
    faqs_dict = {}
    db = shelve.open('faq.db', 'w')
    faqs_dict = db['Faqs']
    faqs_dict.pop(id)
    db['Faqs'] = faqs_dict
    db.close()
    return redirect(url_for('retrieve_faq'))

# <-------------------------------------------------------------------------------------------->
# <------------------------------ Ben's stuff start here -------------------------------------->
# <-------------------------------------------------------------------------------------------->

@app.route('/')
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(basedata.Model, UserMixin):
    id = basedata.Column(basedata.Integer, primary_key=True)
    email = basedata.Column(basedata.String(20), nullable=False, unique=True)
    password = basedata.Column(basedata.String(80), nullable=False)
    type = basedata.Column(basedata.String(1), nullable=False)

    def get_type(self):
        return self.type


class CustomerInfo(basedata.Model):
    id = basedata.Column(basedata.Integer, primary_key=True)
    user_id = basedata.Column(basedata.Integer, basedata.ForeignKey('user.id'))
    first_name = basedata.Column(basedata.String(100))
    last_name = basedata.Column(basedata.String(100))
    address = basedata.Column(basedata.String(150))
    phone = basedata.Column(basedata.Integer)


letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation

alphabet = letters + digits + special_chars

pwd_length = 12

pwd = ''
for i in range(pwd_length):
    pwd += ''.join(secrets.choice(alphabet))

while True:
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))

    if (any(char in special_chars for char in pwd) and
            sum(char in digits for char in pwd) >= 1):
        break
print(pwd)


@app.before_first_request
def create_tables():
    basedata.create_all()
    admin = User.query.filter_by(type='A').first()
    if admin is None:
        tester = Bcrypt.generate_password_hash("test1234")
        admin = User(email="Admin@gmail.com", password=tester, type="A")
        basedata.session.add(admin)
        basedata.session.commit()


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        flash('Reset request sent. Check your mail')
        user.password = bcrypt.generate_password_hash(pwd)
        try:

            basedata.session.commit()
        except:
            pass

    return render_template('reset_request.html', form=form)


class RegisterCustomer(Form):
    first_name = StringField("Customer's First Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField("Customer's Last Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField(validators=[InputRequired(), Email()], render_kw={"placeholder": "Email address"})
    address = StringField('Mailing Address (For us to send you freebies!)',
                            [validators.length(max=200), validators.Optional()])
    phone = IntegerField('Phone Number (Do Not include Country Code)',
                         [validators.NumberRange(min=80000000, max=99999999), validators.Optional()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=16)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=8, max=16),
                                                 equal_to('password', 'Passwords do not match')],
                                     render_kw={"placeholder": "Re-type Password"})

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError('That email already exists. Please choose a different one.')


class LoginForm(Form):
    email = StringField(validators=[InputRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route('/register_customer', methods=['GET', 'POST'])
def register():
    register_customer = RegisterCustomer(request.form)

    if request.method == 'POST' and register_customer.validate():
        hashed_password = bcrypt.generate_password_hash(register_customer.password.data)
        new_user = User(email=register_customer.email.data, password=hashed_password, type="S")
        basedata.session.add(new_user)
        basedata.session.commit()
        new_customer_info = CustomerInfo(user_id=new_user.id, first_name=register_customer.first_name.data,
                                         last_name=register_customer.last_name.data)
        basedata.session.add(new_customer_info)
        basedata.session.commit()

        return redirect(url_for('login'))

    return render_template('sign_up_Customer.html', form=register_customer)


@app.route('/account_details', methods=['GET', 'POST'])
def Customer_details():
    Customerinfo = CustomerInfo.query.all()
    return render_template('retrieveCustomer.html', Customerinfo=Customerinfo)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_Customer():
    create_Customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_Customer_form.validate():
        customers_dict = {}
        db = shelve.open('Customer.db', 'c')
        try:
            customers_dict = db['Customers']
            User.Customer.count_id = db['Customer_count_id']

        except:
            print("Error in retrieving Customers from Customer.db.")

        Customer = User(create_Customer_form.first_name.data,
                        create_Customer_form.last_name.data,
                        create_Customer_form.email.data,
                        create_Customer_form.address.data,
                        create_Customer_form.phone.data,
                        create_Customer_form.password.data, create_Customer_form.confirm_password.data)

        customers_dict[Customer.get_user_id()] = Customer

        db['Customers'] = customers_dict
        db['Customer_count_id'] = Customer.Customer.count_id

        db.close()
        return redirect(url_for('home'))

    return render_template('createCustomer.html', form=create_Customer_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            if user.type == "S":
                return redirect(url_for('edit_profile'))
            elif user.type == "A":
                return redirect(url_for('home'))

        else:
            flash('Invalid email/password. Please try again.')

    return render_template('login.html', form=login_form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    Customerprofile = CustomerInfo.query.filter_by(user_id=current_user.id).first()
    userpw = User.query.filter_by(id=current_user.id).first()
    id = Customerprofile.id
    first_name = Customerprofile.first_name
    last_name = Customerprofile.last_name
    address = Customerprofile.address
    phone = Customerprofile.phone
    hashed_password = userpw.password

    return render_template('edit_profile.html', id=id, first_name=first_name, last_name=last_name,
                           address=address, phone=phone, password=hashed_password)


@app.route('/updateCustomerInfo/<int:id>', methods=['GET', 'POST'])
@login_required
def updateCustomerInfo(id):
    form = RegisterCustomer()
    name_to_update = CustomerInfo.query.filter_by(user_id=current_user.id).first()
    name_to_update1 = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        name_to_update.first_name = request.form['first_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.address = request.form['address']
        name_to_update.phone = request.form['phone']
        name_to_update1.password = request.form['password']
        try:
            name_to_update1.password = bcrypt.generate_password_hash(name_to_update1.password)
            basedata.session.commit()
            flash("User Updated Successfully!")
            return render_template('updateCustomerInfo.html',
                                   form=form,
                                   name_to_update=name_to_update, name_to_update1=name_to_update1, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template('updateCustomerInfo.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
    else:
        return render_template('updateCustomerInfo.html',
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/retrieveCustomers')
def retrieve_Customers():
    customers_dict = {}
    db = shelve.open('Customer.db', 'c')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customers = customers_dict.get(key)
        customers_list.append(customers)

    return render_template('retrieveCustomer.html', count=len(customers_list), Customers_list=customers_list)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_Customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' or update_customer_form.validate():  # 'and' or 'or'
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['customers']
        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_phone(update_customer_form.phone.data)
        db['customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_Customers'))
    else:
        customers_dict = {}
        db = shelve.open('Customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.phone.data = customer.get_phone()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_Customer(id):
    customers_dict = {}
    db = shelve.open('Customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()
    return redirect(url_for('retrieve_Customers'))



if __name__ == '__main__':
    app.run(debug=True)
