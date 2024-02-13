# Creating data model to "stores" relation

"""
CREATE TABLE STORES(

	STORE_ID INTEGER PRIMARY KEY,
    STORE_NAME VARCHAR(255) NOT NULL,
    PHONE VARCHAR(25) NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    STREET VARCHAR(255) NOT NULL,
    CITY VARCHAR(255) NOT NULL,
    STATE VARCHAR(255) NOT NULL,
    ZIP_CODE VARCHAR(10) NOT NULL

)
"""


class Store:
    def __init__(self,store_id: int, store_name: str,
                 phone: str, email: str, street: str,
                 city: str, state: str, zip_code: str):
        self.store_id = store_id
        self.store_name = store_name
        self.phone = phone
        self.email = email
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
