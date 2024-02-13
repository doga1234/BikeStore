class Order:
    def __init__(self, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id,
                 total_price=0):
        self.customer_id = customer_id
        self.order_status = order_status
        self.order_date = order_date
        self.required_date = required_date
        self.shipped_date = shipped_date
        self.store_id = store_id
        self.staff_id = staff_id
        self.total_price = total_price
