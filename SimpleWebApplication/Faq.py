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


