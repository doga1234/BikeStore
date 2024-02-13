class OrderItem:
    def __init__(self, order_id: int, item_id: int, product_id: int, quantity: int, list_price: float,
                 discount: float, net_price: float):
        self.order_id = order_id
        self.item_id = item_id
        self.product_id = product_id
        self.quantity = quantity
        self.list_price = list_price
        self.discount = discount
        self.net_price = net_price
