from dao.order_processor import OrderProcessor
from entity.user import User
from entity.product import Electronics, Clothing


def main():
    processor = OrderProcessor()

    while True:
        print("\n--- Order Management System ---")
        print("1. Create User")
        print("2. Create Product")
        print("3. Create Order")
        print("4. Cancel Order")
        print("5. Get All Products")
        print("6. Get Orders by User")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                user = User(int(input("User ID: ")), input("Username: "), input("Password: "),
                            input("Role (Admin/User): "))
                processor.create_user(user)

            elif choice == '2':
                role = input("Are you an admin? (yes/no): ")
                if role.lower() != 'yes':
                    print("Only admins can add products.")
                    continue
                admin = User(0, "admin", "admin", "Admin")
                type_ = input("Type (Electronics/Clothing): ")
                if type_ == "Electronics":
                    product = Electronics(int(input("Product ID: ")), input("Name: "), input("Description: "),
                                          float(input("Price: ")), int(input("Quantity: ")),
                                          input("Brand: "), int(input("Warranty Period: ")))
                else:
                    product = Clothing(int(input("Product ID: ")), input("Name: "), input("Description: "),
                                       float(input("Price: ")), int(input("Quantity: ")),
                                       input("Size: "), input("Color: "))
                processor.create_product(admin, product)

            elif choice == '3':
                user = User(int(input("User ID: ")), input("Username: "), input("Password: "), "User")
                product_ids = input("Enter product IDs (comma-separated): ").split(',')
                products = []
                for pid in product_ids:
                    products.append(Electronics(int(pid), "", "", 0.0, 0, "", 0))  # dummy, just for product_id
                processor.create_order(user, products)

            elif choice == '4':
                processor.cancel_order(int(input("User ID: ")), int(input("Order ID: ")))

            elif choice == '5':
                for p in processor.get_all_products():
                    print(p)

            elif choice == '6':
                user = User(int(input("User ID: ")), "", "", "User")
                for o in processor.get_order_by_user(user):
                    print(o)

            elif choice == '7':
                print("Exiting...")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
