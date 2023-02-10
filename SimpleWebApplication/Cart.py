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
