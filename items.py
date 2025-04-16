import db

def get_all_classes():
    sql = "SELECT class_name, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for class_name, value in result:
        classes[class_name] = []
    for class_name, value in result:
        classes[class_name].append(value)

    return classes

def add_item(item_name, description, status, user_id, classes):
    sql = "INSERT INTO items (item_name, description,status, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [item_name, description, status, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, item_class_name, value) VALUES (?, ?, ?)"
    for item_class_name, value in classes:
        db.execute(sql, [item_id, item_class_name, value])

def get_items():
    sql = "SELECT id, item_name, status FROM items ORDER BY id DESC"
    return db.query(sql)

def get_classes(item_id):
    sql = "SELECT item_class_name, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_item(item_id):
    sql = """SELECT   items.id,
                    items.item_name,
                    items.description,
                    items.status,
                    users.id AS user_id,
                    users.username
            FROM    items, users
            WHERE   items.user_id = users.id AND
                    items.id = ?"""

    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, item_name, description, status, classes):
    sql = """UPDATE items SET   item_name = ?,
                                description = ?,
                                status = ?
                          WHERE id = ?
                          """
    db.execute(sql, [item_name, description, status, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql="INSERT INTO item_classes (item_id, item_class_name, value) VALUES (?, ?, ?)"
    for item_class_name, value in classes:
        db.execute(sql, [item_id, item_class_name, value])

def remove_item(item_id):
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_item(query):
    sql = """SELECT id, item_name, status
            FROM  items
            WHERE item_name LIKE ? OR description LIKE ?
            ORDER BY id DESC"""

    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def add_claim(item_id, user_id, contact_info):
    sql = "INSERT INTO claims (item_id, user_id, contact_info) VALUES (?, ?, ?)"
    return db.execute(sql, [item_id, user_id, contact_info])

def get_claims(item_id):
    sql = """SELECT claims.contact_info, users.id AS user_id, users.username
           FROM claims, users
           WHERE claims.item_id = ? AND claims.user_id = users.id
           ORDER BY claims.id DESC"""
    return db.query(sql, [item_id])

def get_claim_by_id(claim_id):
    sql = """SELECT id, item_id, user_id, contact_info
             FROM claims
             WHERE id = ?"""
    result = db.query(sql, [claim_id])[0]
    return result if result else None

def get_claim_by_user(item_id, user_id):
    sql = """SELECT id, item_id, user_id, contact_info
             FROM claims
             WHERE item_id = ? AND user_id = ?"""
    result = db.query(sql, [item_id, user_id])[0]
    return result if result else None

def replace_claim(claim_id, new_contact_info):
    sql = """UPDATE claims SET contact_info = ?
                           WHERE id = ?"""
    return db.execute(sql, [new_contact_info, claim_id])