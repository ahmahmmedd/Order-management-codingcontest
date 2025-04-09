import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any
from dao.order_management_repository import OrderManagementRepository
from entity.user import User
from entity.product import Product
from entity.electronics import Electronics
from entity.clothing import Clothing
from exception.usernotfoundexception import UserNotFoundException
from exception.ordernotfound import OrderNotFoundException
from exception.productnotfoundexception import ProductNotFoundException
from util.db_util import connect_db

class OrderProcessor(OrderManagementRepository):
    def __init__(self):
        self.connection = None
        try:
            self.connection = connect_db()
            if not self.connection or not self.connection.is_connected():
                raise Exception("failed to establish database connection")
        except Exception as e:
            print(f"initialization error: {e}")
            if self.connection:
                self.connection.close()
            raise

    def __del__(self):
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()

    def _user_exists(self, user_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "select userid from users where userid = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"error checking user existence: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def _product_exists(self, product_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "select productid from products where productid = %s"
            cursor.execute(query, (product_id,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"error checking product existence: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def _order_exists(self, order_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = "select orderid from orders where orderid = %s"
            cursor.execute(query, (order_id,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"error checking order existence: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def create_user(self, username: str, password: str, role: str) -> int:
        try:
            cursor = self.connection.cursor()
            query = "insert into users (username, password, role) values (%s, %s, %s)"
            cursor.execute(query, (username, password, role))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"error creating user: {e}")
            self.connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def create_product(self, admin_user_id: int, product_data: Dict[str, Any]) -> int:
        try:
            cursor = self.connection.cursor()
            user_check_query = "select userid from users where userid = %s and role = 'admin'"
            cursor.execute(user_check_query, (admin_user_id,))
            admin_user = cursor.fetchone()

            if not admin_user:
                raise UserNotFoundException("admin user not found or doesn't have privileges")

            if product_data['type'].lower() == 'electronics':
                query = """insert into products 
                          (productname, description, price, quantityinstock, type, brand, warrantyperiod) 
                          values (%s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    product_data['product_name'],
                    product_data['description'],
                    product_data['price'],
                    product_data['quantity_in_stock'],
                    'Electronics',
                    product_data['brand'],
                    product_data['warranty_period']
                )
            elif product_data['type'].lower() == 'clothing':
                query = """insert into products 
                          (productname, description, price, quantityinstock, type, size, color) 
                          values (%s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    product_data['product_name'],
                    product_data['description'],
                    product_data['price'],
                    product_data['quantity_in_stock'],
                    'Clothing',
                    product_data['size'],
                    product_data['color']
                )
            else:
                raise ValueError("invalid product type")

            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"error creating product: {e}")
            self.connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def create_order(self, user_id: int, product_ids: List[int]) -> bool:
        if not self._user_exists(user_id):
            raise UserNotFoundException()

        try:
            cursor = self.connection.cursor()
            order_query = "insert into orders (userid) values (%s)"
            cursor.execute(order_query, (user_id,))
            order_id = cursor.lastrowid

            for product_id in product_ids:
                if not self._product_exists(product_id):
                    raise ProductNotFoundException(f"product id {product_id} not found")

                detail_query = "insert into orderdetails (orderid, productid, quantity) values (%s, %s, %s)"
                cursor.execute(detail_query, (order_id, product_id, 1))

                update_query = "update products set quantityinstock = quantityinstock - 1 where productid = %s"
                cursor.execute(update_query, (product_id,))

            self.connection.commit()
            return True
        except Error as e:
            print(f"error creating order: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def cancel_order(self, user_id: int, order_id: int) -> bool:
        if not self._user_exists(user_id):
            raise UserNotFoundException()
        if not self._order_exists(order_id):
            raise OrderNotFoundException()

        try:
            cursor = self.connection.cursor()
            get_products_query = "select productid from orderdetails where orderid = %s"
            cursor.execute(get_products_query, (order_id,))
            product_ids = [row[0] for row in cursor.fetchall()]

            for pid in product_ids:
                update_query = "update products set quantityinstock = quantityinstock + 1 where productid = %s"
                cursor.execute(update_query, (pid,))

            delete_details_query = "delete from orderdetails where orderid = %s"
            cursor.execute(delete_details_query, (order_id,))

            delete_order_query = "delete from orders where orderid = %s"
            cursor.execute(delete_order_query, (order_id,))

            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"error canceling order: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_all_products(self) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "select * from products"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"error fetching products: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_order_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        if not self._user_exists(user_id):
            raise UserNotFoundException()

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """select p.* from products p 
                      join orderdetails od on p.productid = od.productid 
                      join orders o on od.orderid = o.orderid 
                      where o.userid = %s"""
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"error fetching user orders: {e}")
            return []
        finally:
            if cursor:
                cursor.close()