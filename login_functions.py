from flask import current_app

def get_user(email):
    db = current_app.config["dbconfig"]
    user = db.get_staff_by_email(email)
    if user is None:
        user = db.get_customer_by_email(email)
    return user
