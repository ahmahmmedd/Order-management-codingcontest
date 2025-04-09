class Product:
    def __init__(self, product_name, description, price, quantity_in_stock, product_type):
        self._product_name = product_name
        self._description = description
        self._price = price
        self._quantity_in_stock = quantity_in_stock
        self._type = product_type


    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        self._product_name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value >= 0:
            self._price = value
        else:
            raise ValueError("Price cannot be negative")

    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    @quantity_in_stock.setter
    def quantity_in_stock(self, value):
        if value >= 0:
            self._quantity_in_stock = value
        else:
            raise ValueError("Quantity cannot be negative")

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in ["Electronics", "Clothing"]:
            self._type = value
        else:
            raise ValueError("Product type must be either 'Electronics' or 'Clothing'")