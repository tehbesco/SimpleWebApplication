from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Forms import CartItem, PayInfo
import shelve, Cart, os
from flask import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sub',methods=["GET","POST"])
def sub():
    pay_info = PayInfo(request.form)
    if request.method == "POST" and pay_info.validate():
        res = make_response(render_template("resub.html"))
        res.set_cookie("sub", "Y")
        return res
    return render_template('sub.html', form = pay_info)

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
    db = shelve.open("search.db", 'r')
    if "search" in db:
        search = db["search"]
    else:
        db.clear()
        search = ""
    db.close()
    if request.method == "POST":
        data = dict(request.form)
        if "submit-button" in data.keys():
            id = data["submit-button"]
            return redirect(url_for('create_cart', food_id=id))
        elif "search" in data.keys():
            search = data["search"]
            db = shelve.open("search.db",'c')
            db["search"] = search
            db.close()
            page = 1
    else:
        page = request.args.get('page', 1, type=int)
    foods = Foods.query.filter(Foods.name.like('%' + search + '%'))
    pagination = foods.paginate(page=page,per_page=2)
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
    cart_item = CartItem(request.form)
    if request.method == 'POST' and cart_item.validate():
        items_dict = {}
        db = shelve.open('cart.db', 'c')

        try:
            items_dict = db['Items']
        except:
            print("Error in retrieving Items from cart.db.")
        cart = Cart.Cart(name, cart_item.quantity.data, cart_item.remarks.data, price)
        items_dict[cart.get_item_id()] = cart
        db['Items'] = items_dict
        db.close()
        return redirect(url_for('retrieve_cart'))
    return render_template('createCart.html', form=cart_item, name=name)


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

@app.route('/pay' , methods=['GET', 'POST'])
def pay():
    items_dict = {}
    db = shelve.open('cart.db', 'r')
    items_dict = db['Items']
    db.close()
    items_list = []
    ttl = 0
    for key in items_dict:
        ttl += items_dict[key].get_cost()
        item = items_dict.get(key)
        items_list.append(item)
    pay_info = PayInfo(request.form)
    if request.cookies.get("sub") == "Y":
        discount = 15
    else:
        discount = 0
    if request.method == 'POST' and pay_info.validate():
        items_dict = {}
        db = shelve.open('cart.db', 'w')
        items_dict = db['Items']
        items_dict.clear()
        db['Items'] = items_dict
        db.close()
        return redirect(url_for('track'))
    return render_template('pay.html', form = pay_info, items_list=items_list, total=ttl, disc = discount)

@app.route('/track')
def track():
    return render_template('track.html')

if __name__ == '__main__':
    app.run()

