class Product:
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, type_):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.type = type_


class Electronics(Product):
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, brand, warranty_period):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, 'Electronics')
        self.brand = brand
        self.warranty_period = warranty_period


class Clothing(Product):
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, size, color):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, 'Clothing')
        self.size = size
        self.color = color
