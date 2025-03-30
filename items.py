import db

def add_item(item_name, description, user_id):
    sql = "INSERT INTO items (item_name, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [item_name, description, user_id])
