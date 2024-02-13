# Creating data model to "staffs" relation
from flask_login import UserMixin

class Staff(UserMixin):
    def __init__(self, first_name: str,
                 last_name: str, email: str, phone: str,
                 active: bool, store_id: int, manager_id: str, password: str, image='/static/media/profile.png'):

        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.active = active
        self.store_id = store_id
        self.manager_id = manager_id
        self.password = password
        self.image = image
        print(self.manager_id)
        self.is_admin = True if self.manager_id == None else False
        self.is_staff = True

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active
