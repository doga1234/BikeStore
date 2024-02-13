# Creating data model to "stocks" relation

"""
    CREATE TABLE STOCKS(
	STORE_ID INTEGER,
	PRODUCT_ID INTEGER,
	QUANTITY INTEGER NOT NULL,
    PRIMARY KEY (STORE_ID, PRODUCT_ID),

    FOREIGN KEY STORE_ID
    REFERENCES STORES STORE_ID
    ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY PRODUCT_ID
    REFERENCES PRODUCTS PRODUCT_ID
    ON DELETE CASCADE ON UPDATE CASCADE
)
"""


class Stock:
    def __init__(self, store_id: int,
                 product_id: int, quantity: int):
        self.store_id = store_id
        self.product_id = product_id
        self.quantity = quantity
