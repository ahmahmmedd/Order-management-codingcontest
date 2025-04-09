from dao.i_order_management_repository import IOrderManagementRepository
from util.db_util import get_connection
from exception.custom_exceptions import UserNotFoundException, OrderNotFoundException

class OrderProcessor(IOrderManagementRepository):
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT,
                                password TEXT,
                                role TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                product_id INTEGER PRIMARY KEY,
                                product_name TEXT,
                                description TEXT,
                                price REAL,
                                quantity_in_stock INTEGER,
                                type TEXT,
                                extra1 TEXT,
                                extra2 TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                product_id INTEGER,
                                FOREIGN KEY(user_id) REFERENCES users(user_id),
                                FOREIGN KEY(product_id) REFERENCES products(product_id))''')
        self.conn.commit()

    def create_user(self, user):
        self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                            (user.user_id, user.username, user.password, user.role))
        self.conn.commit()

    def create_product(self, user, product):
        if user.role != "Admin":
            raise PermissionError("Only admin can create products.")
        extras = ('', '')
        if product.type == 'Electronics':
            extras = (product.brand, str(product.warranty_period))
        elif product.type == 'Clothing':
            extras = (product.size, product.color)

        self.cursor.execute('''INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (product.product_id, product.product_name, product.description,
                             product.price, product.quantity_in_stock, product.type,
                             extras[0], extras[1]))
        self.conn.commit()

    def create_order(self, user, products):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user.user_id,))
        if not self.cursor.fetchone():
            self.create_user(user)

        for product in products:
            self.cursor.execute("INSERT INTO orders(user_id, product_id) VALUES (?, ?)",
                                (user.user_id, product.product_id))
        self.conn.commit()

    def cancel_order(self, user_id, order_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        if not self.cursor.fetchone():
            raise UserNotFoundException("User not found.")

        self.cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        if not self.cursor.fetchone():
            raise OrderNotFoundException("Order not found.")

        self.cursor.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
        self.conn.commit()

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def get_order_by_user(self, user):
        self.cursor.execute('''SELECT p.* FROM orders o 
                               JOIN products p ON o.product_id = p.product_id 
                               WHERE o.user_id = ?''', (user.user_id,))
        return self.cursor.fetchall()
