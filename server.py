import os
import views
from flask import Flask
from database import Database
from init import *
from flask_login import LoginManager
from login_functions import get_user
from flask_session import Session

db = Database("bike_stores.db")

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
	return get_user(user_id)

if not os.path.exists("./bike_stores.db"):
    #Creating tables according to dataset
    create_tables()
    #Inserting datas according to dataset
    add_brands("csv_files/brands.csv")
    add_categories("csv_files/categories.csv")
    add_customers("csv_files/customers.csv")
    add_order_items("csv_files/order_items_new.csv")
    add_orders("csv_files/orders.csv")   
    add_products("csv_files/products.csv")
    add_staffs("csv_files/staffs.csv")
    add_stocks("csv_files/stocks.csv")
    add_stores("csv_files/stores.csv")
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("settings")
    Session(app)

    #URL Paths in Navbar
    app.add_url_rule("/",view_func=views.home)
    app.add_url_rule("/products", view_func=views.products_page, methods=["GET", "POST"])
    app.add_url_rule("/categories", view_func = views.categories_page,methods = ["GET","POST"])
    app.add_url_rule("/stores", view_func = views.stores_page,methods = ["GET","POST"])
    app.add_url_rule("/brands", view_func = views.brands_page,methods = ["GET","POST"])
    app.add_url_rule("/order_items", view_func = views.order_items_page,methods = ["GET","POST"])
    app.add_url_rule("/staffs",view_func=views.staffs_page, methods = ["GET","POST"])
    app.add_url_rule("/stocks",view_func=views.stocks_page, methods = ["GET","POST"])
    app.add_url_rule("/orders",view_func=views.orders_page, methods = ["GET","POST"])
    
    #URL Paths for Authentication operations
    app.add_url_rule("/sign_in_customer",view_func=views.sign_in_customer,methods = ["GET","POST"])
    app.add_url_rule("/sign_in_staff",view_func=views.sign_in_staff,methods = ["GET","POST"])
    app.add_url_rule("/sign_up",view_func=views.sign_up,methods = ["GET","POST"])
    app.add_url_rule("/sign_out",view_func=views.sign_out)
    app.add_url_rule("/user", view_func=views.customer_profile)
    app.add_url_rule("/deleteuser", view_func=views.delete_customer)
    app.add_url_rule("/updateuser", view_func=views.update_customer, methods=["GET", "POST"])
    app.add_url_rule("/signup_staff_page", view_func=views.signup_staff_page, methods=["GET", "POST"])

    
    
    #URL Paths for CRUD Operations for product
    app.add_url_rule("/new_product", view_func = views.new_product_page,methods = ["GET","POST"])
    app.add_url_rule("/products/<product_id>",view_func=views.product_page, methods = ["GET", "POST"])
    app.add_url_rule("/products/update_product/<product_id>",view_func=views.update_product_page,methods = ["GET","POST"])
    app.add_url_rule("/search_products",view_func=views.search_products,methods = ["GET","POST"])

    #URL Paths for CRUD Operations for category
    app.add_url_rule("/new_category",view_func=views.new_category_page,methods =["GET","POST"])

    #URL Paths for CRUD Operations for store
    app.add_url_rule("/new_store",view_func=views.new_store_page,methods =["GET","POST"])
    app.add_url_rule("/search_stores",view_func=views.search_stores,methods = ["GET","POST"])
    app.add_url_rule("/stores/<store_id>",view_func=views.store_page, methods = ["GET", "POST"])
    app.add_url_rule("/stores/update_store/<store_id>",view_func=views.update_store_page,methods = ["GET","POST"])
    
    #URL Paths for CRUD Operations for brands
    app.add_url_rule("/brands", view_func=views.brands_page, methods=["GET", "POST"])
    app.add_url_rule("/search_brands", view_func=views.search_brands, methods=["GET", "POST"])
    app.add_url_rule("/new_brand", view_func=views.add_brand_page, methods=["GET", "POST"])
    app.add_url_rule("/brands/<brand_id>", view_func=views.brand_page, methods=["GET", "POST"])
    app.add_url_rule("/update_brand/<brand_id>", view_func=views.update_brand, methods=["GET", "POST"])

    #URL Paths for CRUD Operations for ordered items
    app.add_url_rule("/new_order_item", view_func=views.add_order_item_page, methods=["GET", "POST"])
    app.add_url_rule("/search_order_items", view_func=views.search_order_items, methods=["GET", "POST"])
    app.add_url_rule("/order_items/<order_id>-<item_id>", view_func=views.order_item_page, methods=["GET", "POST"])
    app.add_url_rule("/update_order_item/<order_id>-<item_id>", view_func=views.update_order_item,methods=["GET", "POST"])
    app.add_url_rule("/bupdate_order_item/<order_item_id>", view_func=views.bupdate_order_item,methods=["GET", "POST"])

    #URL Paths for CRUD Operations for staffs
    app.add_url_rule("/update_staff/<staff_id>", view_func=views.update_staff, methods=["GET", "POST"])
    app.add_url_rule("/search_staffs", view_func=views.search_staffs, methods=["GET", "POST"])
    app.add_url_rule("/update_staff/<staff_id>", view_func=views.update_staff, methods=["GET", "POST"])
    app.add_url_rule("/staffs/<staff_id>", view_func=views.staff_page, methods=["GET", "POST"])

    #URL Paths for CRUD Operations for stocks
    app.add_url_rule("/search_stocks", view_func=views.search_stocks, methods=["GET", "POST"])
    app.add_url_rule("/update_stock/<store_id>-<product_id>", view_func=views.update_stock, methods=["GET", "POST"])
    app.add_url_rule("/new_stock", view_func=views.add_stock_page, methods=["GET", "POST"])
    app.add_url_rule("/stocks/<store_id>-<product_id>", view_func=views.stock_page, methods=["GET", "POST"])
    
    #URL Paths for CRUD Operations for orders
    app.add_url_rule("/myorders", view_func=views.myorders)
    app.add_url_rule("/orders", view_func=views.orders_page, methods=["GET", "POST"])
    app.add_url_rule("/search_orders", view_func=views.search_order, methods=["GET", "POST"])
    app.add_url_rule("/updateorder/<order_id>", view_func=views.update_order, methods=["GET", "POST"])
    app.add_url_rule("/makeorder", view_func=views.makeorder)

    #URL Paths for Customer Cart, Order
    app.add_url_rule("/myorders", view_func=views.myorders)
    app.add_url_rule("/addtocart/<product_id>", view_func=views.add_to_cart)
    app.add_url_rule("/mycart", view_func=views.mycart, methods=["GET", "POST"])
    app.add_url_rule("/makeorder", view_func=views.makeorder)


    lm.init_app(app)
    lm.login_view = "signin"

    app.config["dbconfig"] = db
    return app

if __name__ == "__main__":
	app = create_app()
	port = app.config.get("PORT", 5000)
	app.run(host="0.0.0.0", port=port)