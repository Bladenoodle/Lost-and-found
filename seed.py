import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM items")
db.execute("DELETE FROM claims")

user_count = 1000
item_count = 10**6
message_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, item_count + 1):
    db.execute("INSERT INTO items (item_name) VALUES (?)",
               ["item" + str(i)])

for i in range(1, message_count + 1):
    user_id = random.randint(1, user_count)
    item_id = random.randint(1, item_count)
    db.execute("""INSERT INTO claims (item_id, user_id, contact_info)
                  VALUES (?, ?, ?)""",
               [user_id, item_id,"message" + str(i)])

db.commit()
db.close()
