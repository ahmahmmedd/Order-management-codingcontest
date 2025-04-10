from entity.product import Product

class Clothing(Product):
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, size, color):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, "Clothing")
        self._size = size
        self._color = color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __str__(self):
        return super().__str__() + f", Size: {self.size}, Color: {self.color}"

