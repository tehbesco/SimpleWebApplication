# Cart class
class Cart:
    count_id = 0

    # initializer method
    def __init__(self, food_name, quantity, remarks, cost):
        Cart.count_id += 1
        self.__item_id = Cart.count_id
        self.__food_name = food_name
        self.__quantity = quantity
        self.__remarks = remarks
        self.__cost = cost

    def __str__(self):
        return self.__food_name
    # accessor methods
    def get_item_id(self):
        return self.__item_id

    def get_food_name(self):
        return self.__food_name

    def get_quantity(self):
        return self.__quantity

    def get_remarks(self):
        return self.__remarks

    def get_cost(self):
        return self.__cost

    # mutator methods
    def set_item_id(self, item_id):
        self.__item_id = item_id

    def set_food_name(self, food_name):
        self.__food_name = food_name

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_cost(self, cost):
        self.__cost = cost


# Order class
class Order:
    count_id = 0

    # initializer method
    def __init__(self, date, restaurant_name, no_of_items, area, remarks, driver_name):
        Order.count_id += 1
        self.__order_id = Order.count_id
        self.__date = date
        self.__restaurant_name = restaurant_name
        self.__no_of_items = no_of_items
        self.__area = area
        self.__driver_name = driver_name
        self.__remarks = remarks

    # accessor methods
    def get_order_id(self):
        return self.__order_id

    def get_date(self):
        return self.__date

    def get_restaurant_name(self):
        return self.__restaurant_name

    def get_no_of_items(self):
        return self.__no_of_items

    def get_area(self):
        return self.__area

    def get_driver_name(self):
        return self.__driver_name

    def get_remarks(self):
        return self.__remarks

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_date(self, date):
        self.__date = date

    def set_restaurant_name(self, restaurant_name):
        self.__restaurant_name = restaurant_name

    def set_no_of_items(self, no_of_items):
        self.__no_of_items = no_of_items

    def set_area(self, area):
        self.__area = area

    def set_driver_name(self, driver_name):
        self.__driver_name = driver_name

    def set_remarks(self, remarks):
        self.__remarks = remarks


# User class
class User:
    count_id = 0

    def __init__(self, first_name, last_name, address, email, phone, password, confirm_password):
        super().__init__(first_name, last_name)
        User.count_id += 1
        self.__User_id = User.count_id
        self.__email = email
        self.__address = address
        self.__phone = phone
        self.__password = password
        self.__confirm_password = confirm_password

    def get_User_id(self):
        return self.__User_id

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def set_User_id(self, User_id):
        self.__User_id = User_id

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def set_password(self, password):
        self.__password = password

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password


# Customer class
class Customer(User):
    count_id = 0

    def __init__(self, first_name, last_name, email, address, phone, password, confirm_password):
        super().__init__(first_name, last_name)
        Customer.count_id += 1
        self.__Customer_id = Customer.count_id
        self.__email = email
        self.__address = address
        self.__phone = phone
        self.__password = password
        self.__confirm_password = confirm_password

    def get_Customer_id(self):
        return self.__Customer_id

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_password(self):
        return self.__password

    def get_confirm_password(self):
        return self.__confirm_password

    def set_Customer_id(self, customer_id):
        self.__Customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def set_password(self, password):
        self.__password = password

    def set_confirm_password(self, confirm_password):
        self.__confirm_password = confirm_password

# FAQ class
class Faq:
    count_id = 0

    def __init__(self, email, remarks):
        Faq.count_id += 1
        self.__faq_id = Faq.count_id
        self.__email = email
        self.__remarks = remarks

    def get_faq_id(self):
        return self.__faq_id

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks

    def set_faq_id(self, faq_id):
        self.__faq_id = faq_id

    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks

