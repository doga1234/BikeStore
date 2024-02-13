import sqlite3
import sqlite3 as dbapi2

from models.category import Category
from models.brands import Brand
from models.products import Product
from models.stocks import Stock
from models.stores import Store
from models.order_items import OrderItem
from models.order import Order
from models.customer import Customer
from models.staffs import Staff


from flask import flash

class Database:
    def __init__(self,dbfile):
        self.dbfile = dbfile
    
    #Emir Sümer
    #CRUD Operations for PRODUCTS Table
    def add_product(self,product):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO PRODUCTS (product_name,brand_id,category_id,model_year,list_price,product_age,warranty) VALUES(?,?,?,?,?,?,?)"
            cursor.execute(statement,(product.product_name,product.brand_id,product.category_id,product.model_year,product.list_price,product.product_age,product.product_warranty,))
            connection.commit()
            product_id = cursor.lastrowid
            cursor.close()
        return product_id
    
    def get_product(self, product_id):
        product = None
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM PRODUCTS WHERE product_id = ?"
            cursor.execute(statement,(product_id,))
            result = cursor.fetchone()
            product = Product(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7])
            cursor.close()
        return product
    
    def delete_product(self,product_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "DELETE FROM PRODUCTS WHERE product_id = ?"
            cursor.execute(statement,(product_id,))
            connection.commit()
            cursor.close()

    def update_product(self,product_id,updated_product):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "UPDATE PRODUCTS SET product_name = ?,brand_id = ?,category_id = ?,model_year = ?,list_price = ?,product_age = ?,warranty = ? WHERE product_id = ?"
            cursor.execute(statement,(updated_product.product_name,updated_product.brand_id,updated_product.category_id,updated_product.model_year,updated_product.list_price,updated_product.product_age,updated_product.product_warranty,product_id,))
            connection.commit()
            cursor.close()
        

    def get_products(self):
        products = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM PRODUCTS ORDER BY product_id"
            cursor.execute(statement)
            for product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty in cursor:
                products.append((product_id,Product(product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty)))
            cursor.close()
        return products
        
    def search_products(self,keyword):
        products = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM PRODUCTS WHERE ((product_name LIKE '%" + keyword + "%')) OR (product_id LIKE '%" + keyword + "%')"
            cursor.execute(statement)
            for product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty in cursor:
                products.append((product_id,Product(product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty)))
            cursor.close()
        return products

    #CRUD Operations for CATEGORIES Table
    def add_category(self,category):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO CATEGORIES (category_name) VALUES(?)"
            cursor.execute(statement,(category.category_name,))
            connection.commit()
            cursor.close()
            
    def get_categories(self):
        categories = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM CATEGORIES ORDER BY category_id"
            cursor.execute(statement)
            for category_id, category_name in cursor:
                categories.append((category_id,category_name))
            cursor.close()
        return categories

    #Doğa Güneş Karadağ
    #CRUD Operations for BRANDS Table
    def add_brand(self, brand: Brand):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BRANDS (BRAND_NAME) VALUES (?)"
            cursor.execute(query, (brand.brand_name,))
            connection.commit()
            brand_key = cursor.lastrowid
            cursor.close()
        return brand_key
     
    def get_brands(self):
        brands = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT BRAND_ID, BRAND_NAME FROM BRANDS ORDER BY BRAND_ID"
            cursor.execute(query)
            for brand_key, brand_name in cursor:
                brands.append((brand_key, Brand(brand_key, brand_name)))
            connection.commit()
            cursor.close()
        return brands 
    
    def get_brand(self, brand_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT BRAND_NAME FROM BRANDS WHERE (BRAND_ID = ?)"
            cursor.execute(query, (brand_key,))
            name = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        brand = Brand(brand_key, name)
        return brand
    
    def delete_brand(self, brand_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BRANDS WHERE (BRAND_ID = ?)"
            cursor.execute(query, (brand_key,))
            connection.commit()
            cursor.close()
            
    def update_brands(self, brand_key, brand: Brand):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE BRANDS SET BRAND_NAME = ? WHERE(BRAND_ID = ?)"
            cursor.execute(query, (brand.brand_name, brand_key))
            connection.commit()
            
    def search_brands(self, keyword):
        brands = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT BRAND_ID, BRAND_NAME FROM BRANDS WHERE ((BRAND_NAME LIKE '%" + keyword + "%') OR (BRAND_ID LIKE '%" + keyword + "%'))"
            cursor.execute(query)
            for brand_key, brand_name in cursor:
                brands.append((brand_key, Brand(brand_key, brand_name)))
            connection.commit()
            cursor.close()
        return brands

   
               
    #CRUD Operations for ORDERS Table
    def add_order(self, order):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ORDERS (CUSTOMER_ID, ORDER_STATUS, ORDER_DATE, REQUIRED_DATE, SHIPPED_DATE," \
                    " STORE_ID, STAFF_ID, TOTAL_PRICE) VALUES (?,?,?,?,?,?,?,?)"
            cursor.execute(query, (order.customer_id, order.order_status, order.order_date, order.required_date,
                                   order.shipped_date, order.store_id, order.staff_id, order.total_price))
            connection.commit()
            order_id = cursor.lastrowid
            cursor.close()
        return order_id
            

    def get_orders(self):
        orders = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ORDERS ORDER BY ORDER_ID"
            cursor.execute(query)
            for _id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id, total_price in cursor:
                orders.append((_id, Order(customer_id, order_status, order_date, required_date, shipped_date,
                                          store_id, staff_id, total_price)))
            cursor.close()
            connection.commit()
        return orders      
    
    def get_order(self, id_):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ORDERS WHERE ORDER_ID = ?"
            cursor.execute(query, (id_, ))
            order_id, customer_id, order_status, order_date, req_date, ship_date, store_id, staff_id, total_price = list(cursor.fetchone())
            cursor.close()
            connection.commit()
        order = Order(customer_id, order_status, order_date, req_date, ship_date, store_id, staff_id, total_price)
        return order
    
    def update_order(self, _id, order: Order):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE ORDERS SET CUSTOMER_ID = ?, ORDER_STATUS = ?, ORDER_DATE = ?, REQUIRED_DATE = ?, " \
                    "SHIPPED_DATE = ?, STORE_ID = ?, STAFF_ID = ?, TOTAL_PRICE = ? WHERE (ORDER_ID = ?)"
            cursor.execute(query, (order.customer_id, order.order_status, order.order_date, order.required_date,
                                   order.shipped_date, order.store_id, order.staff_id, order.total_price, _id))
            cursor.close()
            connection.commit()

    def delete_order(self, _id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ORDERS WHERE (ORDER_ID = ?)"
            cursor.execute(query, (_id,))
            cursor.close()
            connection.commit()

    def get_orders_of_customer(self, _customerid):
        orders = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ORDERS WHERE CUSTOMER_ID = ? ORDER BY ORDER_ID"
            cursor.execute(query, (_customerid, ))
            for _id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id, total_price in cursor:
                orders.append((_id, Order(customer_id, order_status, order_date, required_date, shipped_date,
                                          store_id, staff_id, total_price)))
            cursor.close()
            connection.commit()
        return orders

    def search_orders(self, keyword):
        orders = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ORDERS WHERE (ORDER_ID = ?)"
            cursor.execute(query, (keyword,))
            for _id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id, total_price in cursor:
                orders.append((_id, Order(customer_id, order_status, order_date, required_date, shipped_date,
                                          store_id, staff_id, total_price)))
            connection.commit()
            cursor.close()

        return orders

    def set_total_price_of_order(self, order_id, total_price):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE ORDERS SET TOTAL_PRICE = ? WHERE ORDER_ID = ?"
            cursor.execute(query, (total_price, order_id))
            cursor.close()
            connection.commit()  


    #Emre Çelik
    #CRUD Operations for ORDER_ITEMS Table
    def add_order_item(self, order_item):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ORDER_ITEMS (ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, LIST_PRICE, DISCOUNT, NET_PRICE) VALUES (?,?,?,?,?,?,?)"
            cursor.execute(query, (
                order_item.order_id, order_item.item_id, order_item.product_id, order_item.quantity,
                order_item.list_price, order_item.discount, order_item.net_price,))
            connection.commit()
            cursor.close()

    def get_order_items(self):
        order_items = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT order_id, item_id, product_id, quantity, list_price, discount, net_price FROM ORDER_ITEMS"
            cursor.execute(statement)
            for order_id, item_id, product_id, quantity, list_price, discount, net_price in cursor:
                order_items.append(((order_id, item_id), OrderItem(order_id, item_id, product_id, quantity, list_price, discount, net_price)))
            connection.commit()
            cursor.close()
        return order_items

    def search_order_items(self, keyword):
        order_items = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, LIST_PRICE, DISCOUNT, NET_PRICE FROM ORDER_ITEMS WHERE (ORDER_ID LIKE '%" + keyword + "%')"
            cursor.execute(query)
            for order_id, item_id, product_id, quantity, list_price, discount, net_price in cursor:
                order_items.append(((order_id, item_id), OrderItem(order_id, item_id, product_id,
                                                                   quantity, list_price, discount, net_price)))
            connection.commit()
            cursor.close()
        return order_items
    
    def get_order_item(self, _id, _id2):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, LIST_PRICE, DISCOUNT, NET_PRICE FROM ORDER_ITEMS WHERE(ORDER_ID = ? AND ITEM_ID = ?)"
            cursor.execute(query, (_id, _id2,))
            order_id, item_id, product_id, quantity, list_price, discount, net_price = list(cursor.fetchone())
            connection.commit()
        order_item_ = OrderItem(order_id, item_id, product_id, quantity, list_price, discount, net_price)
        return order_item_

    def delete_order_item(self, order_id,item_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "DELETE FROM ORDER_ITEMS WHERE (order_id = ? AND item_id = ?)"
            cursor.execute(statement, (order_id,item_id,))
            connection.commit()

    def update_order_item(self, _id, _id2, order_item: OrderItem):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE ORDER_ITEMS SET ORDER_ID = ?, ITEM_ID = ?, PRODUCT_ID = ?, QUANTITY = ?, LIST_PRICE = ?, DISCOUNT = ?, NET_PRICE = ? WHERE(ORDER_ID = ? AND ITEM_ID = ?)"
            cursor.execute(query, (order_item.order_id, order_item.item_id, order_item.product_id,
                                   order_item.quantity, order_item.list_price, order_item.discount,
                                   order_item.net_price, _id, _id2))
            connection.commit()


    #CRUD Operations for STORE Table
    def add_store(self, store):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO STORES(store_name, phone, email, street, city, state, zip_code) VALUES (?,?,?,?,?,?,?)"
            cursor.execute(query, (store.store_name, store.phone, store.email, store.street, store.city, store.state, store.zip_code))
            connection.commit()
            store_id = cursor.lastrowid
            cursor.close()
        return store_id

    def get_stores(self):
        stores = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM STORES ORDER BY store_id"
            cursor.execute(statement)
            for store_id, store_name, phone, email, street, city, state, zip_code in cursor:
                stores.append((store_id, Store(store_id,store_name, phone, email, street, city, state, zip_code)))
            cursor.close()
        return stores
    
    def get_store(self, store_id):
        store = None
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM STORES WHERE store_id = ?"
            cursor.execute(statement,(store_id,))
            store_id, store_name, phone, email, street, city, state, zip_code = list(cursor.fetchone())
            connection.commit()
            cursor.close()
        store = Store(store_id, store_name, phone, email, street, city, state, zip_code)
        return store
    
    def update_store(self,store_id,updated_store):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "UPDATE STORES SET store_name = ?,phone = ?,email = ?,street = ?,city = ?,state = ?,zip_code = ? WHERE store_id = ?"
            cursor.execute(statement,(updated_store.store_name,updated_store.phone,updated_store.email,updated_store.street,updated_store.city,updated_store.state,updated_store.zip_code,store_id,))
            connection.commit()
            cursor.close()

    def delete_store(self, store_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "DELETE FROM STORES WHERE store_id = ?"
            cursor.execute(statement, (store_id,))
            connection.commit()
            cursor.close()

    def search_stores(self,keyword):
        stores = list()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            statement = "SELECT * FROM STORES WHERE ((store_id LIKE '%" + keyword + "%')) OR (store_name LIKE '%" + keyword + "%') OR (phone LIKE '%" + keyword + "%') OR (email LIKE '%" + keyword + "%') OR (street LIKE '%" + keyword + "%') OR (city LIKE '%" + keyword + "%') OR (state LIKE '%" + keyword + "%') OR (zip_code LIKE '%" + keyword + "%')"
            cursor.execute(statement)
            for store_id, store_name, phone, email, street, city, state, zip_code in cursor:
                stores.append((store_id,Store(store_id, store_name, phone, email, street, city, state, zip_code)))
            cursor.close()
        return stores
        
    #CRUD Operations for STOCKS Table
    def add_stock(self, stock):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO STOCKS (STORE_ID, PRODUCT_ID, QUANTITY) VALUES (?,?,?)"
            cursor.execute(query, (stock.store_id, stock.product_id, stock.quantity))
            connection.commit()
            store_id = cursor.lastrowid
        return store_id

    def get_stock(self, _id, _id2):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STORE_ID, PRODUCT_ID, QUANTITY FROM STOCKS WHERE(STORE_ID = ? AND PRODUCT_ID = ?)"
            cursor.execute(query, (_id, _id2,))
            store_id, product_id, quantity = list(cursor.fetchone())
            connection.commit()
        stock_ = Stock(store_id, product_id, quantity)
        return stock_

    def get_stocks(self):
        stocks = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STORE_ID, PRODUCT_ID, QUANTITY FROM STOCKS ORDER BY STORE_ID"
            cursor.execute(query)
            for store_id, product_id, quantity in cursor:
                stocks.append((store_id, product_id, Stock(store_id, product_id, quantity)))
            connection.commit()
            cursor.close
        return stocks
    
    def update_stocks(self, _id, _id2, stock: Stock):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE STOCKS SET STORE_ID = ?, PRODUCT_ID = ?, QUANTITY = ? WHERE(STORE_ID = ? AND PRODUCT_ID = ?)"
            cursor.execute(query, (stock.store_id, stock.product_id, stock.quantity, _id, _id2))
            connection.commit()
    
    def search_stocks(self,keyword):
        stocks = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STORE_ID, PRODUCT_ID, QUANTITY FROM STOCKS WHERE ((STORE_ID LIKE '%"+keyword+"%'))"
            cursor.execute(query)
            for store_id, product_id, quantity in cursor:
                stocks.append((store_id, product_id, Stock(store_id, product_id, quantity)))
            connection.commit()
            cursor.close()
        return stocks
    
    def delete_stock(self, _id, _id2):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM STOCKS WHERE (STORE_ID = ? AND PRODUCT_ID = ?)"
            cursor.execute(query, (_id, _id2,))
            connection.commit()


    # Ozan Çetin
    # CRUD Operations for STAFFS Table

    def get_staff(self, _id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE, STORE_ID, MANAGER_ID, PASSWORD, IMAGE FROM STAFFS WHERE(STAFF_ID = ?)"
            cursor.execute(query, (_id,))
            fname, lname, email, phone, active, store_id, manager_id, pw, image = list(cursor.fetchone())
            cursor.close()
            connection.commit()
        staff_ = Staff(fname, lname, email, phone, active, store_id, manager_id, pw, image)
        staff_.id = _id
        return staff_

    def get_staffs(self):
        staffs = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STAFF_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE, STORE_ID, MANAGER_ID,PASSWORD, IMAGE FROM STAFFS ORDER BY STAFF_ID"
            cursor.execute(query)
            for staff_id, first_name, last_name, email, phone, active, store_id, manager_id, password, image in cursor:
                staffs.append((staff_id,
                               Staff(first_name, last_name, email, phone, active, store_id, manager_id,
                                     password, image)))
            connection.commit()
            cursor.close()
        return staffs       

    def get_staffs(self):
        staffs = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STAFF_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE, STORE_ID, MANAGER_ID,PASSWORD, IMAGE FROM STAFFS ORDER BY STAFF_ID"
            cursor.execute(query)
            for staff_id, first_name, last_name, email, phone, active, store_id, manager_id, password, image in cursor:
                staffs.append((staff_id,
                                Staff(first_name, last_name, email, phone, active, store_id, manager_id,
                                        password, image)))
            connection.commit()
            cursor.close()
        return staffs

    def get_staff_by_email(self,email):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STAFF_ID, FIRST_NAME, LAST_NAME, PHONE, EMAIL , ACTIVE, STORE_ID, MANAGER_ID, PASSWORD, IMAGE FROM STAFFS WHERE (EMAIL = ?)"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result is not None:
                id_, fname, lname, phone, email, active, store_id, manager_id, pw, image = list(result)
                staff_ = Staff(fname, lname, email, phone, active, store_id, manager_id, pw, image)
                staff_.id = id_
            else:
                staff_ = None
            cursor.close()
            connection.commit()
        return staff_

    def add_staff(self, staff):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO STAFFS(FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE, STORE_ID, MANAGER_ID, PASSWORD, IMAGE) VALUES(?,?,?,?,?,?,?,?,?)"
            cursor.execute(query, (
            staff.first_name, staff.last_name, staff.email, staff.phone, staff.active, staff.store_id, staff.manager_id,
            staff.password, staff.image))
            connection.commit()
            staff_id = cursor.lastrowid
            cursor.close()

    def update_staffs(self, _id, staff: Staff):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE STAFFS  SET FIRST_NAME = ?, LAST_NAME = ?, EMAIL = ?, PHONE = ?, ACTIVE = ?, STORE_ID = ?, MANAGER_ID = ? WHERE (STAFF_ID = ?)"
            cursor.execute(query, (
            staff.first_name, staff.last_name, staff.email, staff.phone, staff.active, staff.store_id, staff.manager_id,
            _id))
            connection.commit()

    def delete_staff(self, _id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM STAFFS WHERE (STAFF_ID = ?)"
            cursor.execute(query, (_id,))
            connection.commit()


    def search_staffs(self, keyword):
        staffs = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STAFF_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE, STORE_ID, MANAGER_ID, PASSWORD FROM STAFFS WHERE ((FIRST_NAME LIKE '%" + keyword + "%') OR (STAFF_ID LIKE '%" + keyword + "%'))"
            cursor.execute(query)
            for staff_id, first_name, last_name, email, phone, active, store_id, manager_id, password in cursor:
                staffs.append((staff_id,
                               Staff(first_name, last_name, email, phone, active, store_id, manager_id,
                                     password)))
            connection.commit()
            cursor.close()
        return staffs        
    
    # CRUD Operations for CUSTOMERS Table
    def get_customer_by_email(self,email):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, PHONE, EMAIL, STREET, CITY, STATE, ZIP_CODE, PASSWORD, " \
                    "IMAGE FROM CUSTOMERS WHERE (EMAIL = ?)"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result is not None:
                id_, fname, lname, phone, email, street, city, state, zipcode, pw, image = list(result)
                customer_ = Customer(fname, lname, phone, email, street, city, state, zipcode, pw, image)
                customer_.id = id_
            else:
                customer_ = None
            cursor.close()
            connection.commit()
        return customer_

    def add_customer(self, customer):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO CUSTOMERS (FIRST_NAME, LAST_NAME, PHONE, EMAIL, STREET, CITY, STATE, ZIP_CODE," \
                    "PASSWORD, IMAGE) VALUES (?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query, (customer.first_name, customer.last_name, customer.phone, customer.email,
                                   customer.street, customer.city, customer.state, customer.zip_code, customer.password,
                                   customer.image))
            connection.commit()
            cursor.close()

    def update_customer(self, _id, customer: Customer):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE CUSTOMERS SET FIRST_NAME = ?, LAST_NAME = ?, PHONE = ?, EMAIL = ?, STREET = ?, CITY = ?, " \
                    "STATE = ?, ZIP_CODE = ?, PASSWORD = ?, IMAGE = ? WHERE (CUSTOMER_ID = ?)"
            cursor.execute(query, (customer.first_name, customer.last_name, customer.phone, customer.email,
                                   customer.street, customer.city, customer.state, customer.zip_code, customer.password,
                                   customer.image, _id))
            cursor.close()
            connection.commit()

    def delete_customer(self, _id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CUSTOMERS WHERE (CUSTOMER_ID = ?)"
            cursor.execute(query, (_id,))
            cursor.close()
            connection.commit()


    #CRUD Operations for Customer Purchase system

    def get_quantities_of_product(self, product_id):
        stats = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STOCKS.STORE_ID, STOCKS.QUANTITY FROM PRODUCTS JOIN STOCKS ON " \
                    "(PRODUCTS.PRODUCT_ID = STOCKS.PRODUCT_ID) WHERE PRODUCTS.PRODUCT_ID = ?"
            cursor.execute(query, (product_id,))
            for store_id, quantity in cursor:
                stats.append((store_id, quantity))
            connection.commit()
            cursor.close()
        return stats
    
    def get_staffid_by_store(self, store_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STAFFS.STAFF_ID FROM STORES JOIN STAFFS ON (STAFFS.STORE_ID = STORES.STORE_ID) WHERE " \
                    "STORES.STORE_ID = ?"
            cursor.execute(query, (store_id,))
            staff_id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return staff_id

    def get_max_item_id(self, order_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT MAX(ITEM_ID) FROM ORDER_ITEMS WHERE (ORDER_ID = ?) GROUP BY(ORDER_ID)"
            cursor.execute(query, (order_id,))
            max_id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        max_id += 1
        return max_id

    def purchase_product(self, product_id, store_id, quantity):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE STOCKS SET QUANTITY = QUANTITY - ? WHERE PRODUCT_ID = ? AND STORE_ID = ?"
            cursor.execute(query, (quantity, product_id, store_id))
            connection.commit()
            cursor.close()


    def get_product_name_of_customers_orders(self, order_id):
        product_names = tuple()
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PRODUCTS.PRODUCT_NAME FROM ORDER_ITEMS JOIN PRODUCTS ON " \
                    "(ORDER_ITEMS.PRODUCT_ID = PRODUCTS.PRODUCT_ID) WHERE (ORDER_ITEMS.ORDER_ID = ?)"
            cursor.execute(query, (order_id,))
            for i in cursor:
                product_names += i
            #print(product_names)
            connection.commit()
            cursor.close()
        return product_names

    def get_store_name_of_order(self, order_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT STORES.STORE_NAME FROM ORDERS JOIN STORES ON (ORDERS.STORE_ID = STORES.STORE_ID)" \
                    "WHERE ORDERS.ORDER_ID = ?"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()[0]
        return result