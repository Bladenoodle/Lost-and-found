import db

def add_item(item_name, description, status, user_id):
    sql="INSERT INTO items (item_name, description,status, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [item_name, description, status, user_id])

def get_items():
    sql="""SELECT id, item_name, status FROM items ORDER BY id DESC"""

    return db.query(sql)

def get_item(item_id):
    sql="""SELECT items.item_name,
                    items.description,
                    items.status,
                    users.username
            FROM    items, users
            WHERE   items.user_id=users.id AND
                    items.id=?"""

    return db.query(sql, [item_id])[0]