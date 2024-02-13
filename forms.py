from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,FileField,IntegerField,FloatField,RadioField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

class NewProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    brand_id = IntegerField("Brand ID",validators=[DataRequired()])
    category_id = IntegerField("Product ID",validators=[DataRequired()])
    model_year = IntegerField("Model Year",validators=[DataRequired()])
    list_price = FloatField("List Price",validators=[DataRequired()])

class NewCategoryForm(FlaskForm):
    category_name = StringField("Category Name",validators=[DataRequired()])

class SignInForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])

class SignUpForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    surname = StringField("Surname",validators=[DataRequired()])
    phone = StringField("Phone")
    email = StringField("Email",validators=[DataRequired()])
    street = StringField("Street",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    image = FileField("Profile Image")

class SignupForm_Staff(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone = StringField("Phone")
    email = StringField("Email", validators=[DataRequired()])
    active = RadioField("Active", validators=[DataRequired()], choices=[(0, "Not active"), (1, "Active")])
    store_id = StringField("Store ID", validators=[DataRequired()])
    manager_id = StringField("Manager ID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    image = FileField("Profile Image")

class NewStoreForm(FlaskForm):
    store_name = StringField("Store Name", validators=[DataRequired()])
    phone = StringField("Phone",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    street = StringField("Street",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])    
    state = StringField("State", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    
class UpdateOrderForm(FlaskForm):
    order_status = IntegerField("Order Status", validators=[DataRequired()])
    shipped_date = StringField("Shipped Date", validators=[DataRequired()])
    staff_id = IntegerField("Staff Id", validators=[DataRequired()])

class UpdateBrandForm(FlaskForm):
    # brand_id = IntegerField("Brand ID", validators=[DataRequired()])
    brand_name = StringField("Brand Name", validators=[DataRequired()])

class UpdateStaffForm(FlaskForm):
    # staff_id = IntegerField("Staff ID", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    active = StringField("active", validators=[DataRequired()])
    store_id = IntegerField("Store ID", validators=[DataRequired()])
    manager_id = StringField("Manager ID", validators=[DataRequired()])

class UpdateOrderItemForm(FlaskForm):
    order_id = IntegerField("Order ID", validators=[DataRequired()])
    item_id = IntegerField("Item ID", validators=[DataRequired()])
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    list_price = FloatField("List Price", validators=[DataRequired()])
    discount = FloatField("Discount")
    net_price = FloatField("Net Price", validators=[DataRequired()])

class UpdateStockForm(FlaskForm):
    store_id = IntegerField("Store ID", validators=[DataRequired()])
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])

class UpdateCustomerForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone = StringField("Phone")
    email = StringField("Email", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])
    image = FileField("Profile Image")