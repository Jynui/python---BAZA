import sqlite3

class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_name: str, quantity: int):
        self.items[product_name] = self.items.get(product_name, 0) + quantity

    def clear_cart(self):
        self.items = {}

    def get_cart(self) -> dict:
        return self.items

class NikeStore:
    DATABASE_PATH = "nike_store.db"

    def __init__(self, database_path: str = DATABASE_PATH):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    total_price REAL NOT NULL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_product(self, name: str, price: float, quantity: int):
        try:
            existing_product = self.get_product_by_name(name)

            if existing_product:
                self.update_product(name, new_quantity=quantity)
                print(f"Quantity of product '{name}' updated successfully.")
            else:
                self.cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
                self.conn.commit()
                print(f"Product '{name}' added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")

    def get_product_by_name(self, name: str):
        self.cursor.execute("SELECT * FROM products WHERE name=?", (name,))
        return self.cursor.fetchone()

    # ... (other methods remain the same)

nike_store = NikeStore()

nike_store.add_product("Air Max Sneakers", 120, 20)
nike_store.add_product("Tech Fleece Hoodie", 80, 15)
nike_store.add_product("Running Shorts", 30, 25)

print("Available products:")
for product in nike_store.get_available_products():
    print(product)

cart = Cart()
cart.add_item("Air Max Sneakers", 2)
cart.add_item("Running Shorts", 3)

print("\nCurrent state of the cart:")
print(cart.get_cart())

nike_store.create_order(customer_name='John Doe', products=cart.get_cart())

print("\nAvailable products after order creation:")
for product in nike_store.get_available_products():
    print(product)

print("\nOrders:")
for order in nike_store.get_orders():
    print(order)
