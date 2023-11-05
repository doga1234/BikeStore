from flask_login import UserMixin


class Customer(UserMixin):
    def __init__(self, first_name, last_name, phone, email, street, city, state, zip_code, password,
                 image='/static/media/profile.png'):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.password = password
        self.image = image
        self.active = True
        self.is_admin = False
        self.is_staff = False

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active
