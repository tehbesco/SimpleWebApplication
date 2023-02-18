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
