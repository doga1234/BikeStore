from flask import render_template, current_app, flash, request, url_for, redirect, session, abort
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
import os
from database import Database
from forms import *
from models.products import Product
from models.brands import Brand
from models.stores import Store
from models.category import Category
from models.order_items import OrderItem
from models.customer import Customer
from models.staffs import Staff
from models.order import Order
from models.stocks import Stock


def home():
    return render_template("index.html")

def sign_up():
	db = current_app.config["dbconfig"]
	form = SignUpForm()
	if form.validate_on_submit():
		email = form.data["email"]
		is_customer_exists = db.get_customer_by_email(email)
		if is_customer_exists is None:
			first_name = form.data["name"]
			last_name = form.data["surname"]
			phone = form.data["phone"]
			email = form.data["email"]
			street = form.data["street"]
			city = form.data["city"]
			state = form.data["state"]
			zip = form.data["zip"]
			password = form.data["password"]
			crypto_password = hasher.hash(password)
			image = request.files["image"]
			if image:
				filename = secure_filename(image.filename)
				tmp = filename.rsplit(".",1)[0]
				ext = filename.rsplit(".",1)[1]
				while os.path.exists(os.path.join(current_app.config["UPLOAD_FOLDER"],(tmp + "." + ext))):
					tmp += "1"
				filename = tmp + "." + ext
				stored_filename = os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
				image.save(os.path.join(current_app.config["UPLOAD_FOLDER"],filename))
			else:
				stored_filename = '/static/media/profile.png'
			customer = Customer(first_name,last_name,phone,email,street,city,state,zip,crypto_password,stored_filename)
			db.add_customer(customer)
			flash("Signed Up succesfully.")
			return redirect(url_for("sign_in_customer",form = form))
		flash("User already exists")
	return render_template("signup.html",form = form)

def sign_in_customer():
	db = current_app.config["dbconfig"]
	form = SignInForm()
	if form.validate_on_submit():
		email = form.data["email"]
		customer = db.get_customer_by_email(email)
		if customer is not None:
			password = form.data["password"]
			if hasher.verify(password,customer.password):
				login_user(customer)
				flash("You have signed in")
				next_page = request.args.get("next",url_for("home"))
				session["cart"] = list()
				return redirect(next_page)
			flash("Invalid email or password")
	return render_template("sign_in_customer.html",form = form)

def sign_in_staff():
	db = current_app.config["dbconfig"]
	form = SignInForm()
	if form.validate_on_submit():
		email = form.data["email"]
		staff = db.get_staff_by_email(email)
		if staff is not None:
			password = form.data["password"]
			if hasher.verify(password,staff.password):
				login_user(staff)
				flash("You have signed in")
				return redirect(url_for("home"))
		flash("Invalid email or password")
	return render_template("sign_in_staff.html",form = form)


@login_required
def signup_staff_page():
	if not current_user.is_admin:
		abort(401)
	form = SignupForm_Staff()
	if form.validate_on_submit():
		print("Entered validation")
		email = form.data["email"]
		checkstaff = current_app.config["dbconfig"].get_staff_by_email(email)
		if checkstaff is None:
			fname = form.data["first_name"]
			lname = form.data["last_name"]
			phone = form.data["phone"] if form.data["phone"] != "" else "nan"
			active = form.data["active"]
			store_id = form.data["store_id"]
			manager_id = form.data["manager_id"]
			password = form.data["password"]
			hashedpw = hasher.hash(password)
			staff_ = Staff(fname, lname, phone, email, active, store_id, manager_id, hashedpw)
			current_app.config["dbconfig"].add_staff(staff_)
			flash("New staff member registered")
			return redirect(url_for("staffs_page"))
		flash("A staff member with that email already exists")
	return render_template("staffsignup.html", form=form)

@login_required
def customer_profile():
	return render_template("customer_profile.html")

@login_required
def update_customer():
	form = UpdateCustomerForm()
	if form.validate_on_submit():
		#print("Entered validation")
		email = form.data["email"]
		checkcustomer = current_app.config["dbconfig"].get_customer_by_email(email)
		if email == current_user.email or checkcustomer is None:
			fname = form.data["first_name"]
			lname = form.data["last_name"]
			phone = form.data["phone"] if form.data["phone"] != "" else "nan"
			street = form.data["street"]
			city = form.data["city"]
			state = form.data["state"]
			zipcode = form.data["zip"]
			password = current_user.password
			image = request.files['image']
			if image:
				filename = secure_filename(image.filename)
				tmp = filename.rsplit('.', 1)[0]
				ext = filename.rsplit('.', 1)[1]
				while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], (tmp+"."+ext))):
					tmp += "1"
				filename = tmp + "." + ext
				fullname = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
				image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
			else:
				fullname = '/static/media/profile.png'
			customer_ = Customer(fname, lname, phone, email, street, city, state, zipcode, password, fullname)
			customer_.id = current_user.id
			current_app.config["dbconfig"].update_customer(customer_.id, customer_)
			flash("Information updated successfully")
			return redirect(url_for("customer_profile"))
		flash("A user with that email already exists")
	form.first_name.data = current_user.first_name
	form.last_name.data = current_user.last_name
	form.phone.data = current_user.phone if current_user.phone != "nan" else ""
	form.email.data = current_user.email
	form.street.data = current_user.street
	form.city.data = current_user.city
	form.state.data = current_user.state
	form.zip.data = current_user.zip_code
	return render_template("customerupdate.html", form=form)

@login_required
def delete_customer():
	db = current_app.config["dbconfig"]
	db.delete_customer(current_user.id)
	flash("You have deleted your profile")
	return redirect(url_for("home"))	

@login_required
def sign_out():
	logout_user()
	flash("You have signed out.")
	return redirect(url_for("home"))

def products_page():
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		products = db.get_products()
		return render_template("products.html", products=products)
	else:
		form_product_keys = request.form.getlist("product_keys")
		if(len(form_product_keys)) == 0:
			flash("Products not selected.")
		else:
			for form_product_key in form_product_keys:
				db.delete_product(int(form_product_key))
		return redirect(url_for("products_page"))

@login_required
def update_product_page(product_id):
	db = current_app.config["dbconfig"]
	product = db.get_product(product_id)
	form = NewProductForm()
	if form.validate_on_submit():
		product_name = form.data["product_name"]
		brand_id = form.data["brand_id"]
		category_id = form.data["category_id"]
		model_year = form.data["model_year"]
		list_price = form.data["list_price"]
		product_age = datetime.today().year - model_year
		product_warranty = 0
		if product_age < 5:
			product_warranty = 1
		updated_product = Product(product_id,product_name,brand_id,category_id,model_year,list_price,product_age,product_warranty)
		db.update_product(product_id,updated_product)
		return redirect(url_for("products_page"))
	form.product_name.data = product.product_name
	form.brand_id.data =  product.brand_id
	form.category_id.data =  product.category_id
	form.model_year.data =  product.model_year
	form.list_price.data =  product.list_price
	return render_template("product_update.html",form = form)

@login_required
def new_product_page():
	db = current_app.config["dbconfig"]
	form = NewProductForm()
	if form.validate_on_submit():
		product_name = form.data["product_name"]
		brand_id = form.data["brand_id"]
		category_id = form.data["category_id"]
		model_year = form.data["model_year"]
		list_price = form.data["list_price"]
		product_age = datetime.today().year - model_year
		product_warranty = 0
		if product_age < 5:
			product_warranty = 1
		product_id = db.add_product(Product(-1, product_name, brand_id, category_id,model_year,list_price,product_age,product_warranty))
		return redirect(url_for("product_page",product_id = product_id))
	return render_template("new_product.html",form = form)

def search_products():
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		form_product_keys = request.form.getlist("product_keys")
		if form_product_keys:
			for form_product_key in form_product_keys:
				db.delete_product(int(form_product_key))
			return redirect(url_for("products_page"))
		keyword = request.form.get("keyword")
		products = db.search_products(keyword)
		if not len(products):
			flash("No result occurred for given keyword: " + keyword)
			products = db.get_products()
			return render_template("products.html",products = products)
	return render_template("products.html",products = products)

@login_required
def product_page(product_id):
	db = current_app.config["dbconfig"]
	product = db.get_product(product_id)
	if request.method == "GET":
		return render_template("product.html", product = product)

@login_required
def brands_page():
	if not current_user.is_admin:
		abort(401)
	mydb = current_app.config["dbconfig"]
	if request.method == "GET":
		brands = mydb.get_brands()
		return render_template("brands.html", brands=sorted(brands))
	else:
		form_brand_keys = request.form.getlist("brand_keys")
		for form_brand_key in form_brand_keys:
			mydb.delete_brand(int(form_brand_key))
		return redirect(url_for("brands_page"))

@login_required
def search_brands():
	if not current_user.is_admin:
		abort(401)
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		form_brand_keys = request.form.getlist("brand_keys")

		if form_brand_keys:
			for form_brand_key in form_brand_keys:
				db.delete_brand(int(form_brand_key))
			return redirect(url_for("brands_page"))

		keyword = request.form.get("keyword")
		brands = db.search_brands(keyword)
		print(brands)
		if not len(brands):
			flash("Could not find any data about given keyword: '" + keyword+"'")
			brands = db.get_brands()
			return render_template("brands.html", brands=brands)

	return render_template("brands.html", brands=brands)

@login_required
def update_brand(brand_id):
	if not current_user.is_admin:
		abort(401)
	brand = current_app.config["dbconfig"].get_brand(brand_id)

	form = UpdateBrandForm()
	if form.validate_on_submit():
		# br_id = form.data["brand_id"]
		br_name = form.data["brand_name"]
		brand_ = Brand(brand_id, br_name)
		current_app.config["dbconfig"].update_brands(brand.brand_id, brand_)
		return redirect(url_for("brands_page"))

	# form.brand_id.data =  brand.brand_id
	form.brand_name.data =  brand.brand_name
	return render_template("brands-update.html", form=form)

@login_required
def brand_page(brand_id):
	if not current_user.is_admin:
		abort(401)
	db = current_app.config["dbconfig"]
	brand = db.get_brand(brand_id)
	if brand is None:
		abort(404)
	return render_template("brand.html", brand=brand)

@login_required
def add_brand_page():
	if not current_user.is_admin:
		abort(401)
	form = UpdateBrandForm()

	if form.validate_on_submit():
		brand_name = form.data["brand_name"]
		db = current_app.config["dbconfig"]
		brand_id = db.add_brand(Brand(-1, brand_name))
		return redirect(url_for("brand_page", brand_id=brand_id))

	return render_template("brands-update.html", form=form)


@login_required
def staff_page(staff_id):
	if (not current_user.is_admin) and (int(current_user.id) != int(staff_id)):
		abort(401)
	db = current_app.config["dbconfig"]
	staff = db.get_staff(staff_id)
	if staff is None:
		abort(404)
	return render_template("staff.html", staff=staff)

@login_required
def staffs_page():
	if not current_user.is_admin:
		abort(401)
	else:
		db = current_app.config["dbconfig"]
		if request.method == "GET":
			staffs = db.get_staffs()
			return render_template("staffs.html", staffs=sorted(staffs))
		else:
			form_staff_keys = request.form.getlist("staff_keys")
			if len(form_staff_keys) == 0:
				flash("Select staff members to delete")
			else:
				for form_staff_key in form_staff_keys:
					db.delete_staff(int(form_staff_key))
			return redirect(url_for("staffs_page"))
		

@login_required
def search_staffs():
	if not current_user.is_admin:
		abort(401)
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		# if not current_user.is_admin:
		# 	abort(401)
		form_staff_keys = request.form.getlist("staff_keys")

		if form_staff_keys:
			for form_staff_keys in form_staff_keys:
				db.delete_staff(int(form_staff_keys))
			return redirect(url_for("staffs_page"))

		keyword = request.form.get("keyword")
		staffs = db.search_staffs(keyword)
		if not len(staffs):
			flash("Could not find any data about given keyword: '" + keyword+"'")
			staffs = db.get_staffs()
			return render_template("staffs.html", staffs=staffs)

	return render_template("staffs.html", staffs=staffs)

@login_required
def update_staff(staff_id):
	if not current_user.is_admin:
		abort(401)
	staff = current_app.config["dbconfig"].get_staff(staff_id)

	form = UpdateStaffForm()
	if form.validate_on_submit():
		print("--------------------")
		# br_id = form.data["brand_id"]
		first_name = form.data["first_name"]
		last_name = form.data["last_name"]
		email = form.data["email"]
		phone = form.data["phone"]
		active = form.data["active"]
		store_id = form.data["store_id"]
		manager_id = form.data["manager_id"]
		password = staff.password
		image = '/static/media/profile.png'
		staff_ = Staff(first_name, last_name, email, phone, active, store_id, manager_id, password, image)
		staff_.id = staff_id
		current_app.config["dbconfig"].update_staffs(staff.id, staff_)
		print("--------------------")
		return redirect(url_for("staffs_page"))

	# form.brand_id.data =  brand.brand_id
	form.first_name.data =  staff.first_name
	form.last_name.data = staff.last_name
	form.email.data = staff.email
	form.phone.data = staff.phone
	form.active.data = staff.active
	form.store_id.data = staff.store_id
	form.manager_id.data = staff.manager_id

	return render_template("staff-update.html", form=form)

@login_required
def order_items_page():
	if not current_user.is_admin:
		abort(401)
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		order_items = db.get_order_items()
		return render_template("order_items.html", order_items=order_items)
	else:
		# if not current_user.is_admin:
		# 	abort(401)
		form_order_item_keys = request.form.getlist("order_item_keys")
		if len(form_order_item_keys) == 0:
			flash("Select order items to delete")
		else:
			for form_order_item_key in form_order_item_keys:
				order_id_, item_id_ = form_order_item_key.split(',')
				db.delete_order_item(int(order_id_), int(item_id_))
		return redirect(url_for("order_items_page"))

@login_required
def search_order_items():
	if not current_user.is_admin:
		abort(401)
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]

		form_order_item_keys = request.form.getlist("order_item_keys")
		if form_order_item_keys:
			for form_order_item_key in form_order_item_keys:
				order_id_, item_id_ = form_order_item_key.split(',')
				db.delete_order_item(int(order_id_), int(item_id_))
			return redirect(url_for("order_items_page"))

		keyword = request.form.get("keyword")
		order_items = db.search_order_items(keyword)
		if not len(order_items):
			flash("Could not find any data about given keyword: '" + keyword+"'")
			order_items = db.get_order_items()
			return render_template("order_items.html", order_items=order_items)

	return render_template("order_items.html", order_items=order_items)

@login_required
def order_item_page(order_id, item_id):
	if not current_user.is_admin:
		abort(401)
	db = current_app.config["dbconfig"]
	order_item = db.get_order_item(order_id, item_id)
	if order_item is None:
		abort(404)
	return render_template("order-item.html", order_item=order_item)
	
@login_required
def add_order_item_page():
	if not current_user.is_admin:
		abort(401)
	form = UpdateOrderItemForm()

	if form.validate_on_submit():
		order_id = form.data["order_id"]
		item_id = form.data["item_id"]
		product_id = form.data["product_id"]
		quantity = form.data["quantity"]
		list_price = form.data["list_price"]
		discount = form.data["discount"]
		net_price = form.data["net_price"]
		db = current_app.config["dbconfig"]
		order_id_ = db.add_order_item(OrderItem(order_id, item_id, product_id,
													quantity, list_price,
													discount, net_price))
		return redirect(url_for("order_item_page", order_id=order_id, item_id=item_id))

	return render_template("order-items-update.html", form=form)
	
def stores_page():
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		stores = db.get_stores()
		return render_template("stores.html", stores=stores)
	else:
		form_store_keys = request.form.getlist("store_keys")
		print(form_store_keys)
		if(len(form_store_keys)) == 0:
			flash("Stores not selected.")
		else:
			for form_store_key in form_store_keys:
				db.delete_store(int(form_store_key))
		return redirect(url_for("stores_page"))
	
@login_required	
def store_page(store_id):
	db = current_app.config["dbconfig"]
	store = db.get_store(store_id)
	if request.method == "GET":
		return render_template("store.html", store = store)
	
@login_required
def new_store_page():
	db = current_app.config["dbconfig"]
	form = NewStoreForm()
	if form.validate_on_submit():
		store_name = form.data["store_name"]
		phone = form.data["phone"]
		email = form.data["email"]
		street = form.data["street"]
		city = form.data["city"]
		state = form.data["state"]
		zip_code = form.data["zip_code"]
		store_id = db.add_store(Store(-1,store_name,phone,email,street,city,state,zip_code))
		return redirect(url_for("stores_page",store_id = store_id))
	return render_template("new_store.html",form = form)

def search_stores():
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		form_store_keys = request.form.getlist("store_keys")
		if form_store_keys:
			for form_store_key in form_store_keys:
				db.delete_store(int(form_store_key))
			return redirect(url_for("stores_page"))
		keyword = request.form.get("keyword")
		stores = db.search_stores(keyword)
		if not len(stores):
			flash("No result occurred for given keyword: " + keyword)
			stores = db.get_stores()
			return render_template("stores.html",stores = stores)
	return render_template("stores.html",stores = stores)
	
@login_required
def update_store_page(store_id):
	db = current_app.config["dbconfig"]
	store = db.get_store(store_id)
	form = NewStoreForm()
	if form.validate_on_submit():
		store_name = form.data["store_name"]
		phone = form.data["phone"]
		email = form.data["email"]
		street = form.data["street"]
		city = form.data["city"]
		state = form.data["state"]
		zip_code = form.data["zip_code"]
		updated_store = Store(store_id,store_name,phone,email,street,city,state,zip_code)
		db.update_store(store_id,updated_store)
		return redirect(url_for("stores_page"))
	form.store_name.data = store.store_name
	form.phone.data =  store.phone
	form.email.data =  store.email
	form.street.data =  store.street
	form.city.data =  store.city
	form.state.data =  store.state
	form.zip_code.data =  store.zip_code
	return render_template("store_update.html",form = form)

@login_required
def stocks_page():
	if not current_user.is_staff:
		abort(401)
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		stocks = db.get_stocks()
		return render_template("stocks.html", stocks=stocks)
	else:
		form_stock_keys = request.form.getlist("stock_keys")
		for form_stock_key in form_stock_keys:
			store_id, product_id = form_stock_key.split(',')
			db.delete_stock(int(store_id),int(product_id))
		return redirect(url_for("stocks_page"))
	
@login_required
def search_stocks():
	if not current_user.is_staff:
		abort(401)
		
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		form_stock_keys = request.form.getlist("stock_keys")

		if form_stock_keys:
			for form_stock_key in form_stock_keys:
				store_id, product_id = form_stock_key.split(',')
				db.delete_stock(int(store_id),int(product_id))
			return redirect(url_for("stocks_page"))

		keyword = request.form.get("keyword")
		stocks = db.search_stocks(keyword)
		if not len(stocks):
			flash("Could not find any data about given keyword: '" + keyword+"'")
			stocks = db.get_stocks()
			return render_template("stocks.html", stocks=stocks)

	return render_template("stocks.html", stocks=stocks)


@login_required
def update_stock(store_id, product_id):
	if not current_user.is_staff:
		abort(401)
	stock = current_app.config["dbconfig"].get_stock(store_id,product_id)

	form = UpdateStockForm()
	if form.validate_on_submit():
		quantity = form.data["quantity"]
		stock_ = Stock(store_id, product_id, quantity)
		current_app.config["dbconfig"].update_stocks(stock.store_id, stock.product_id, stock_)
		return redirect(url_for("stocks_page"))

	# form.brand_id.data =  brand.brand_id
	form.store_id.data = store_id
	form.product_id.data = product_id
	form.quantity.data = stock.quantity
	return render_template("stocks-update.html", form=form)


@login_required
def stock_page(store_id, product_id):
	if not current_user.is_staff:
		abort(401)
	db = current_app.config["dbconfig"]
	stock = db.get_stock(store_id, product_id)
	if stock is None:
		abort(404)
	return render_template("stock.html", stock=stock)


@login_required
def add_stock_page():
	if not current_user.is_staff:
		abort(401)
	form = UpdateStockForm()

	if form.validate_on_submit():
		store_id = form.data["store_id"]
		product_id = form.data["product_id"]
		quantity = form.data["quantity"]
		db = current_app.config["dbconfig"]
		stock_id = db.add_stock(Stock(store_id,product_id,quantity))
		return redirect(url_for("stock_page", store_id = store_id, product_id = product_id))

	return render_template("stocks-update.html", form = form)


	
@login_required
def orders_page():
	if not current_user.is_staff:
		abort(401)
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		orders = db.get_orders()
		return render_template("orders.html", orders=orders)
	else:
		form_order_keys = request.form.getlist("order_keys")
		if len(form_order_keys) == 0:
			flash("Select order records to delete")
		else:
			for form_order_key in form_order_keys:
				db.delete_order(int(form_order_key))
		return redirect(url_for("orders_page"))

@login_required
def search_order():
	if not current_user.is_staff:
		abort(401)
	if request.method == "GET":
		return redirect(url_for("home"))
	else:
		db = current_app.config["dbconfig"]
		form_order_keys = request.form.getlist("order_keys")
		if len(form_order_keys) == 0:
			pass
		else:
			for form_order_key in form_order_keys:
				db.delete_order(int(form_order_key))
			return redirect(url_for("orders_page"))
		keyword = request.form.get("keyword")
		orders = db.search_orders(keyword)
		if not len(orders):
			flash("Could not find any data about given keyword: '" + keyword+"'")
			return redirect(url_for("orders_page"))

	return render_template("orders.html", orders=orders)

@login_required
def myorders():
	if current_user.is_staff:
		abort(401)
	else:
		db = current_app.config["dbconfig"]
		orders = db.get_orders_of_customer(current_user.id)
		for i in range(len(orders)):
			orders[i] = list(orders[i])
			orders[i].append(db.get_product_name_of_customers_orders(orders[i][0]))
			orders[i].append(db.get_store_name_of_order(orders[i][0]))

		return render_template("myorders.html", orders=orders)


@login_required
def update_order(order_id):
	if not current_user.is_staff:
		abort(401)
	form = UpdateOrderForm()
	db = current_app.config["dbconfig"]
	old_order = db.get_order(order_id)
	if old_order is None:
		abort(404)

	if form.validate_on_submit():
		order_status = form.data["order_status"]
		shipped_date = form.data["shipped_date"]
		staff_id = form.data["staff_id"]
		old_order.order_status = order_status
		old_order.shipped_date = shipped_date
		old_order.staff_id = staff_id
		db.update_order(order_id, old_order)
		return redirect(url_for("orders_page"))

	form.order_status.data = old_order.order_status
	form.shipped_date.data = old_order.shipped_date
	form.staff_id.data = old_order.staff_id

	return render_template("order_update.html", form=form)


@login_required
def update_order_item(order_id,item_id):
	if not current_user.is_admin:
		abort(401)
	order_item = current_app.config["dbconfig"].get_order_item(order_id, item_id)

	form = UpdateOrderItemForm()
	if form.validate_on_submit():
		or_id = form.data["order_id"]
		it_id = form.data["item_id"]
		pr_id = form.data["product_id"]
		quan = form.data["quantity"]
		list_pr = form.data["list_price"]
		disc = form.data["discount"]
		net_pr = form.data["net_price"]
		order_item_ = OrderItem(order_id, item_id, pr_id, quan, list_pr, disc, net_pr)
		current_app.config["dbconfig"].update_order_item(order_item.order_id, order_item.item_id, order_item_)
		return redirect(url_for("order_items_page"))

	form.order_id.data =  order_item.order_id
	form.item_id.data =  order_item.item_id
	form.product_id.data =  order_item.product_id
	form.quantity.data =  order_item.quantity
	form.list_price.data =  order_item.list_price
	form.discount.data =  order_item.discount
	form.net_price.data =  order_item.net_price
	return render_template("order-items-update.html", form=form)

@login_required
def bupdate_order_item(order_item_id):
	order_item_id = order_item_id.lstrip("(")
	order_item_id = order_item_id.rstrip(")")
	order_id = order_item_id.split(",")[0]
	item_id = order_item_id.split(",")[1]
	if not current_user.is_admin:
		abort(401)
	order_item = current_app.config["dbconfig"].get_order_item(order_id, item_id)

	form = UpdateOrderItemForm()
	if form.validate_on_submit():
		or_id = form.data["order_id"]
		it_id = form.data["item_id"]
		pr_id = form.data["product_id"]
		quan = form.data["quantity"]
		list_pr = form.data["list_price"]
		disc = form.data["discount"]
		net_pr = form.data["net_price"]
		order_item_ = OrderItem(order_id, item_id, pr_id, quan, list_pr, disc, net_pr)
		current_app.config["dbconfig"].update_order_item(order_item.order_id, order_item.item_id, order_item_)
		return redirect(url_for("order_items_page"))

	form.order_id.data =  order_item.order_id
	form.item_id.data =  order_item.item_id
	form.product_id.data =  order_item.product_id
	form.quantity.data =  order_item.quantity
	form.list_price.data =  order_item.list_price
	form.discount.data =  order_item.discount
	form.net_price.data =  order_item.net_price
	return render_template("order-items-update.html", form=form)

@login_required
def categories_page():
	db = current_app.config["dbconfig"]
	if request.method == "GET":
		categories = db.get_categories()
		return render_template("categories.html",categories = categories)

@login_required
def new_category_page():
	db = current_app.config["dbconfig"]
	form = NewCategoryForm()
	if form.validate_on_submit():
		category_name = form.data["category_name"]
		db.add_category(Category(category_name))
		return redirect(url_for("categories_page"))
	return render_template("new_category.html",form = form)
		

@login_required
def myorders():
	if current_user.is_staff:
		abort(401)
	else:
		db = current_app.config["dbconfig"]
		orders = db.get_orders_of_customer(current_user.id)
		for i in range(len(orders)):
			orders[i] = list(orders[i])
			orders[i].append(db.get_product_name_of_customers_orders(orders[i][0]))
			orders[i].append(db.get_store_name_of_order(orders[i][0]))

		return render_template("myorders.html", orders=orders)

@login_required
def add_to_cart(product_id):
	db = current_app.config["dbconfig"]
	product_ = db.get_product(product_id)
	quantity_list = db.get_quantities_of_product(product_id)
	total_quantity = 0
	for i in quantity_list:
		total_quantity += i[1]
	if total_quantity == 0:
		flash("Out of stock.")
	else:
		session["cart"].append(product_)
		flash("Added to your cart.")
	return redirect(url_for("products_page"))

@login_required
def mycart():
	if request.method == "GET":
		return render_template("mycart.html")
	else:
		form_product_ids = request.form.getlist("cart_keys")
		for product_id_ in form_product_ids:
			for product in session["cart"]:
				if product.product_id == int(product_id_):
					print(product.product_id)
					session["cart"].remove(product)
		return render_template("mycart.html")

@login_required
def makeorder():
	if len(session["cart"]) == 0:
		flash("Your cart is empty!")
		return redirect(url_for("mycart"))
	db = current_app.config["dbconfig"]
	quantities = {}
	for i in session["cart"]:
		if i.product_id in quantities.keys():
			quantities[i.product_id] += 1
		else:
			quantities[i.product_id] = 1
	list_prices = {}
	for i in session["cart"]:
		if i.product_id in quantities.keys():
			list_prices[i.product_id] = i.list_price

	store_candidates = []
	for key in quantities:
		for i in db.get_quantities_of_product(key):
			if i[1] >= quantities[key]:
				if i[0] not in store_candidates:
					store_candidates.append(int(i[0]))
			else:
				if i[0] in store_candidates:
					store_candidates.remove(int(i[0]))
	if len(store_candidates) == 0:
		flash("We do not have these items in any stores.")
		return redirect(url_for("mycart"))

	store_id = store_candidates[0]
	staff_id = db.get_staffid_by_store(store_id)
	required_date = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day+3)
	new_order = Order(current_user.id, 3, datetime.now().date().__str__(), required_date, "nan", store_id, staff_id)
	order_id = db.add_order(new_order)

	total_price = 0
	for item in quantities:
		item_id = db.get_max_item_id(item)
		net_price = list_prices[item]
		total_price += net_price
		new_order_item = OrderItem(order_id, item_id, item, quantities[item], list_prices[item], 20, net_price)
		db.add_order_item(new_order_item)
		db.purchase_product(item, store_id, quantities[item])
	total_price = round(total_price,2)
	db.set_total_price_of_order(order_id, total_price)

	session["cart"] = []
	flash("You ordered successfully.")
	return redirect(url_for("myorders"))