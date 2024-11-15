from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://User00:Coen6313@cluster0.4otmd.mongodb.net/")

# Access the database and collections
db = client.order_management
user_collection = db.users
order_collection = db.orders

# Sample data for users
users_data = [
    {"user_id": "U001", "name": "Alice Smith", "email": "alice.smith@example.com", "delivery_address": "123 Main St, CityA, CountryA"},
    {"user_id": "U002", "name": "Bob Johnson", "email": "bob.johnson@example.com", "delivery_address": "456 Oak St, CityB, CountryB"},
    {"user_id": "U003", "name": "Charlie Brown", "email": "charlie.brown@example.com", "delivery_address": "789 Pine St, CityC, CountryC"},
    {"user_id": "U004", "name": "Diana Prince", "email": "diana.prince@example.com", "delivery_address": "101 Maple St, CityD, CountryD"},
    {"user_id": "U005", "name": "Edward Elric", "email": "edward.elric@example.com", "delivery_address": "202 Birch St, CityE, CountryE"}
]

# Sample data for orders
orders_data = [
    {"order_id": "O1001", "user_id": "U001", "items": ["book", "pen"], "email": "alice.smith@example.com", "delivery_address": "123 Main St, CityA, CountryA", "status": "under process"},
    {"order_id": "O1002", "user_id": "U002", "items": ["laptop", "mouse"], "email": "bob.johnson@example.com", "delivery_address": "456 Oak St, CityB, CountryB", "status": "shipping"},
    {"order_id": "O1003", "user_id": "U003", "items": ["phone", "charger"], "email": "charlie.brown@example.com", "delivery_address": "789 Pine St, CityC, CountryC", "status": "delivered"},
    {"order_id": "O1004", "user_id": "U004", "items": ["headphones", "USB cable"], "email": "diana.prince@example.com", "delivery_address": "101 Maple St, CityD, CountryD", "status": "under process"},
    {"order_id": "O1005", "user_id": "U005", "items": ["notebook", "pencil"], "email": "edward.elric@example.com", "delivery_address": "202 Birch St, CityE, CountryE", "status": "shipping"}
]

# Insert users and orders into MongoDB
user_collection.insert_many(users_data)
order_collection.insert_many(orders_data)

print("Inserted 5 users and 5 orders into MongoDB.")
