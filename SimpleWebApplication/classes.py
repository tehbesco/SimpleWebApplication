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
