class Product:
    def __init__(self,product_id:int,product_name: str,brand_id: int,category_id: int, model_year:int,list_price:float,product_age:int,product_warranty:bool):
        self.product_id = product_id
        self.product_name = product_name
        self.brand_id = brand_id
        self.category_id = category_id
        self.model_year = model_year
        self.list_price = list_price
        self.product_age = product_age
        self.product_warranty = product_warranty