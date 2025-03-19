import csv
from tabulate import tabulate

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, amount):
        self.quantity += amount

class Inventory:
    def __init__(self, filename="inventory.csv"):
        self.filename = filename
        self.products = self.load_inventory()

    def load_inventory(self):
        products = {}
        try:
            with open(self.filename, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) == 4:
                        products[row[0]] = Product(row[0], row[1], float(row[2]), int(row[3]))
        except FileNotFoundError:
            open(self.filename, 'w').close()
        return products

    def save_inventory(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Product ID", "Name", "Price", "Quantity"])
            for product in self.products.values():
                writer.writerow([product.product_id, product.name, product.price, product.quantity])

    def add_product(self, product_id, name, price, quantity):
        if product_id in self.products:
            print("Product ID already exists!")
        else:
            self.products[product_id] = Product(product_id, name, price, quantity)
            self.save_inventory()
            print("Product added successfully!")

    def display_inventory(self):
        if not self.products:
            print("Inventory is empty!")
            return
        table = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        print(tabulate(table, headers=["Product ID", "Name", "Price", "Quantity"], tablefmt="grid"))

class SalesManager:
    def __init__(self, inventory, filename="sales.csv"):
        self.filename = filename
        self.inventory = inventory
        self.sales = self.load_sales()

    def load_sales(self):
        sales = []
        try:
            with open(self.filename, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) == 5:
                        sales.append(row)
        except FileNotFoundError:
            open(self.filename, 'w').close()
        return sales

    def save_sales(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Quantity Sold", "Total Price"])
            writer.writerows(self.sales)

    def process_sale(self):
        sale_id = input("Enter Sale ID: ")
        items = []
        while True:
            product_id = input("Enter Product ID to sell (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            if product_id in self.inventory.products:
                try:
                    quantity = int(input(f"Enter quantity for {self.inventory.products[product_id].name}: "))
                    if quantity > self.inventory.products[product_id].quantity:
                        print("Insufficient stock!")
                    else:
                        product = self.inventory.products[product_id]
                        total_price = product.price * quantity
                        items.append([sale_id, product_id, product.name, quantity, total_price])
                        product.update_quantity(-quantity)
                except ValueError:
                    print("Invalid quantity! Please enter a valid number.")
            else:
                print("Invalid Product ID!")
        self.sales.extend(items)
        self.save_sales()
        self.inventory.save_inventory()
        print("Sale recorded successfully!")

    def display_sales(self):
        if not self.sales:
            print("No sales recorded yet!")
            return
        print(tabulate(self.sales, headers=["Sale ID", "Product ID", "Product Name", "Quantity Sold", "Total Price"], tablefmt="grid"))

class Shop:
    def __init__(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager(self.inventory)

    def menu(self):
        while True:
            print("\n--- Small Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product")
            print("3. Process Sale")
            print("4. View Sales")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inventory.display_inventory()
            elif choice == "2":
                product_id = input("Enter Product ID: ")
                name = input("Enter Product Name: ")
                try:
                    price = float(input("Enter Price: "))
                    quantity = int(input("Enter Quantity: "))
                    self.inventory.add_product(product_id, name, price, quantity)
                except ValueError:
                    print("Invalid input! Please enter valid numbers for price and quantity.")
            elif choice == "3":
                self.sales_manager.process_sale()
            elif choice == "4":
                self.sales_manager.display_sales()
            elif choice == "5":
                print("Exiting... Thank you!")
                break
            else:
                print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    Shop().menu()
