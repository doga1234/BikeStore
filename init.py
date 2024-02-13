import sqlite3 as dbapi2
from database import *
from models.category import Category
from models.products import Product
from models.staffs import Staff
from models.customer import Customer
from models.order import Order
from models.brands import Brand
from models.stocks import Stock
from models.stores import Store
from models.order_items import OrderItem
import csv

dbfile = "bike_stores.db"
db = Database(dbfile)

#Creates tables in database according to csv files.
def create_tables():
    with dbapi2.connect(dbfile) as connection:
        cursor = connection.cursor()

        statement = "CREATE TABLE IF NOT EXISTS BRANDS (" \
                    "brand_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "brand_name VARCHAR(50) NOT NULL" \
                    ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS CATEGORIES (" \
                    "category_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "category_name VARCHAR(50) NOT NULL" \
                    ")"
        
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS CUSTOMERS (" \
                "customer_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "first_name VARCHAR(50) NOT NULL," \
                "last_name VARCHAR(50) NOT NULL," \
                "phone VARCHAR(25)," \
                "email VARCHAR(50) NOT NULL UNIQUE," \
                "street VARCHAR(50)," \
                "city VARCHAR(50)," \
                "state VARCHAR(50)," \
                "zip_code VARCHAR(5)," \
                "password VARCHAR," \
                "image VARCHAR(150)" \
                ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS ORDER_ITEMS(" \
                    "order_id INTEGER,"\
                    "item_id INTEGER," \
                    "product_id INTEGER NOT NULL,"\
                    "quantity INTEGER NOT NULL,"\
                    "list_price DECIMAL(10,2) NOT NULL,"\
                    "discount DECIMAL(10,2) NOT NULL,"\
                    "net_price DECIMAL(10,2) NOT NULL,"\
                    "item_image VARCHAR(150) DEFAULT 'No Image',"\
                    "FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE ON UPDATE CASCADE,"\
                    "FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE ON UPDATE CASCADE"\
                    ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS ORDERS (" \
                    "order_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "customer_id INTEGER," \
                    "order_status INTEGER NOT NULL," \
                    "order_date VARCHAR(10) NOT NULL," \
                    "required_date VARCHAR(10) NOT NULL," \
                    "shipped_date VARCHAR(10) NOT NULL," \
                    "store_id INTEGER NOT NULL," \
                    "staff_id INTEGER NOT NULL," \
                    "total_price DECIMAL(10,2),"\
                    "FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                    "FOREIGN KEY (store_id) REFERENCES stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                    "FOREIGN KEY (staff_id) REFERENCES staffs (staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION" \
                    ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS PRODUCTS("\
                    "product_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "product_name VARCHAR(50) NOT NULL,"\
                    "brand_id INTEGER NOT NULL,"\
                    "category_id INTEGER NOT NULL,"\
                    "model_year DECIMAL(4) NOT NULL,"\
                    "list_price DECIMAL(10,2) NOT NULL,"\
                    "product_age INTEGER NOT NULL,"\
                    "warranty BOOLEAN NOT NULL CHECK (warranty IN(0,1)),"\
                    "FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE ON UPDATE CASCADE,"\
                    "FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE ON UPDATE CASCADE"\
                    ")"
        cursor.execute(statement)
        
        statement = "CREATE TABLE IF NOT EXISTS STAFFS("\
                    "staff_id INTEGER PRIMARY KEY AUTOINCREMENT,"\
                    "first_name VARCHAR(50) NOT NULL,"\
                    "last_name VARCHAR(50) NOT NULL,"\
                    "email VARCHAR(50) NOT NULL UNIQUE,"\
                    "phone VARCHAR(50) NOT NULL UNIQUE,"\
                    "active SMALLINT NOT NULL,"\
                    "store_id INTEGER NOT NULL,"\
                    "manager_id INTEGER,"\
                    "password VARCHAR NOT NULL,"\
                    "image VARCHAR(150),"\
                    "FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE ON UPDATE CASCADE,"\
                    "FOREIGN KEY (manager_id) REFERENCES STAFFS(staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION"\
                    ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS STOCKS("\
                    "store_id INTEGER NOT NULL,"\
                    "product_id INTEGER NOT NULL,"\
                    "quantity INTEGER,"\
                    "FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE ON DELETE CASCADE,"\
                    "FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE ON UPDATE CASCADE"\
                    ")"
        cursor.execute(statement)

        statement = "CREATE TABLE IF NOT EXISTS STORES ("\
                    "store_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"\
                    "store_name VARCHAR(50) NOT NULL,"\
                    "phone VARCHAR(50) NOT NULL UNIQUE,"\
                    "email VARCHAR(50) NOT NULL UNIQUE,"\
                    "street VARCHAR(50) NOT NULL,"\
                    "city VARCHAR(50) NOT NULL,"\
                    "state VARCHAR(50) NOT NULL,"\
                    "zip_code VARCHAR(10) NOT NULL"\
                    ")"
        cursor.execute(statement)
        
        statement = "CREATE TABLE IF NOT EXISTS ORDERS (" \
                "order_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "customer_id INTEGER," \
                "order_status INTEGER NOT NULL," \
                "order_date VARCHAR(10) NOT NULL," \
                "required_date VARCHAR(10) NOT NULL," \
                "shipped_date VARCHAR(10) NOT NULL," \
                "store_id INTEGER NOT NULL," \
                "staff_id INTEGER NOT NULL," \
                "total_price DECIMAL(10, 2)," \
                "FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                "FOREIGN KEY (store_id) REFERENCES stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                "FOREIGN KEY (staff_id) REFERENCES staffs (staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION" \
                ")"
        cursor.execute(statement)
        
        statement = """CREATE TABLE IF NOT EXISTS BRANDS(
            BRAND_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BRAND_NAME VARCHAR(80) NOT NULL
            )"""
        cursor.execute(statement)
        cursor.close()
        connection.commit()
        
#Reading from csv files
def add_products(filepath):
    products = list()
    #Reads csv file
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                products.append(row[0].split(";"))
            counter+=1
        for row in products:
            #Initializes model
            product_id = row[0]
            product_name = row[1]
            brand_id = row[2]
            category_id = row[3]
            model_year = row[4]
            list_price = row[5]
            product_age = row[6]
            product_warranty = row[7]
            product = Product(product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty)
            #calls insert function from database
            db.add_product(product)

def add_categories(filepath):
    categories = list()
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                categories.append(row[0].split(";"))
            counter +=1
    for row in categories:
        db.add_category(Category(row[1]))
        
def add_order_items(filepath):
    order_items = list()
    #Reads csv file
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                order_items.append(row[0].split(";"))
            counter+=1
        for row in order_items:
            #Initializes model
            order_id = row[0]
            item_id = row[1]
            product_id = row[2]
            quantity = row[3]
            list_price = row[4]
            discount = row[5]
            net_price = row[6]
            order_item = OrderItem(order_id,item_id,product_id,quantity,list_price,discount,net_price)
            #calls insert function from database
            db.add_order_item(order_item)

def add_stores(filepath):
    stores = list()
    #Reads csv file
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                stores.append(row[0].split(";"))
            counter+=1
            
        for row in stores:
            #Initializes model
            store_id = row[0]
            store_name = row[1]
            phone = row[2]
            email = row[3]
            street = row[4]
            city = row[5]
            state = row[6]
            zip_code = row[7]
            store = Store(store_id,store_name,phone,email,street,city,state,zip_code)
            #calls insert function from database
            db.add_store(store)

def add_stocks(filepath):
    stocks = list()
    #Reads csv file
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                stocks.append(row[0].split(";"))
            counter+=1
        for row in stocks:
            #Initializes model
            store_id = row[0]
            product_id = row[1]
            quantity = row[2]
            stock = Stock(store_id,product_id,quantity)
            #calls insert function from database
            db.add_stock(stock)

def add_staffs(filepath):
    staff_members = list()
    # Read CSV file
    with open(filepath, "r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if counter != 0:
                staff_members.append(row[0].split(";"))
            counter += 1
    for row in staff_members:
        staff_id = row[0]
        first_name = row[1]
        last_name = row[2]
        email = row[3]
        phone = row[4]
        active = bool(int(row[5]))  # 1 for active or 0 for inactive
        store_id = int(row[6])  # Assuming store_id is an integer
        manager_id = row[7] if row[7] != '' else None
        password = row[8]
        image = row[9] if row[9] != '' else '/static/media/profile.png'  # Default image if empty
        staff = Staff(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            active=active,
            store_id=store_id,
            manager_id=manager_id,
            password=password,
            image=image
        )
        db.add_staff(staff)

def add_customers(filepath):
    customers_list = list()
    # Read CSV file
    with open(filepath, "r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if counter != 0:
                customers_list.append(row[0].split(";"))
            counter += 1
    for row in customers_list:
        first_name = row[1]
        last_name = row[2]
        phone = row[3]
        email = row[4]
        street = row[5]
        city = row[6]
        state = row[7]
        zip_code = row[8]
        password = row[9]
        image = row[10] if row[10] != '' else '/static/media/profile.png'  # Default image if empty

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            password=password,
            image=image
        )
        db.add_customer(customer)
        
def add_brands(filepath):
    brands = list()
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                brands.append(row[0].split(";"))
            counter+=1
        for row in brands:
            brand_id=row[0]
            brand_name =row[1]
            db.add_brand(Brand(brand_id, brand_name))
        
def add_orders(filepath):
    orders = list()
    with open(filepath,"r") as file:
        csvreader = csv.reader(file)
        counter = 0
        for row in csvreader:
            if(counter != 0):
                orders.append(row[0].split(";"))
            counter +=1
    for row in orders:
        customer_id = row[1]
        order_status = row[2]
        order_date = row[3]
        required_date = row[4]
        shipped_date = row[5]
        store_id = row[6]
        staff_id = row[7]
        total_price = row[8]
        order = Order(customer_id,order_status,order_date,required_date,shipped_date,store_id,staff_id,total_price)
        db.add_order(order)



