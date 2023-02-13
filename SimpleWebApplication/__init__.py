from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from flask import *
import pandas as pd
import openpyxl

from datetime import date, datetime
from collections import Counter
from math import ceil
from Forms import CartItem, PayInfo, CreateOrderForm
from classes import *
import shelve, os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

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


if __name__ == '__main__':
    app.run()
