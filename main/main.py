from dao.order_processor import OrderProcessor
from exception.usernotfoundexception import UserNotFoundException
from exception.ordernotfound import OrderNotFoundException


class MainModule:
    def __init__(self):
        self.order_processor = OrderProcessor()

    def display_menu(self):
        print("\nOrder Management System")
        print("1. Create User")
        print("2. Create Product (Admin only)")
        print("3. Create Order")
        print("4. Cancel Order")
        print("5. Get All Products")
        print("6. Get Orders by User")
        print("7. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    self.create_user()
                elif choice == "2":
                    self.create_product()
                elif choice == "3":
                    self.create_order()
                elif choice == "4":
                    self.cancel_order()
                elif choice == "5":
                    self.get_all_products()
                elif choice == "6":
                    self.get_orders_by_user()
                elif choice == "7":
                    print("Exiting the system...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {e}")

    def create_user(self):
        print("\nCreate New User")
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (Admin/User): ").capitalize()

        user_id = self.order_processor.create_user(username, password, role)
        if user_id != -1:
            print(f"User created successfully with ID: {user_id}")
        else:
            print("Failed to create user")

    def create_product(self):
        print("\nCreate New Product (Admin Only)")
        admin_id = int(input("Enter your admin user ID: "))

        product_type = input("Enter product type (Electronics/Clothing): ").lower()
        product_data = {
            'product_name': input("Enter product name: "),
            'description': input("Enter description: "),
            'price': float(input("Enter price: ")),
            'quantity_in_stock': int(input("Enter quantity in stock: ")),
            'type': product_type
        }

        if product_type == "electronics":
            product_data['brand'] = input("Enter brand: ")
            product_data['warranty_period'] = int(input("Enter warranty period (months): "))
        elif product_type == "clothing":
            product_data['size'] = input("Enter size: ")
            product_data['color'] = input("Enter color: ")
        else:
            print("Invalid product type")
            return

        product_id = self.order_processor.create_product(admin_id, product_data)
        if product_id != -1:
            print(f"Product created successfully with ID: {product_id}")
        else:
            print("Failed to create product")

    def create_order(self):
        print("\nCreate New Order")
        user_id = int(input("Enter your user ID: "))

        product_ids = [int(pid.strip()) for pid in input("Enter product IDs to order: ").split(',')]

        if self.order_processor.create_order(user_id, product_ids):
            print("Order created successfully!")
        else:
            print("Failed to create order")

    def cancel_order(self):
        print("\nCancel Order")
        user_id = int(input("Enter your user ID: "))
        order_id = int(input("Enter order ID to cancel: "))

        if self.order_processor.cancel_order(user_id, order_id):
            print("Order cancelled successfully!")
        else:
            print("Failed to cancel order")

    def get_all_products(self):
        print("\nAll Products")
        products = self.order_processor.get_all_products()
        for product in products:
            print(f"ID: {product['productId']}, Name: {product['productName']}, Price: {product['price']}")

    def get_orders_by_user(self):
        print("\nOrders by User")
        user_id = int(input("Enter user ID: "))
        orders = self.order_processor.get_order_by_user(user_id)
        for order in orders:
            print(f"ID: {order['productId']}, Name: {order['productName']}")


if __name__ == "__main__":
    app = MainModule()
    app.run()