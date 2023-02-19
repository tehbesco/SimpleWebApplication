import User


class Customer(User.User):
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

