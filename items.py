import db

def add_item(item_name, description, status, user_id, classes, upload_time, edit_time):
    sql = "INSERT INTO items (item_name, description, status, user_id, upload_time, edit_time) VALUES (?, ?, ?, ?, ?, ?)"
    cursor = db.execute(sql, [item_name, description, status, user_id, upload_time, edit_time])

    item_id = cursor.lastrowid

    sql = "INSERT INTO item_classes (item_id, item_class_name, value) VALUES (?, ?, ?)"
    for item_class_name, value in classes:
        db.execute(sql, [item_id, item_class_name, value])

    return item_id


def get_items():
    sql = """
    SELECT items.id,
           items.item_name,
           items.status,
           items.upload_time,
           items.edit_time,
           users.id AS user_id,
           users.username AS uploader,
           (SELECT classes.value
            FROM item_classes
            JOIN classes ON item_classes.value = classes.value
            WHERE item_classes.item_id = items.id
              AND classes.class_name = 'Where'
            LIMIT 1) AS location
    FROM items
    LEFT JOIN users ON items.user_id = users.id
    ORDER BY items.id DESC
    """
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.item_name,
                    items.description,
                    items.status,
                    items.upload_time,
                    items.edit_time,
                    users.id AS user_id,
                    users.username
            FROM    items, users
            WHERE   items.user_id = users.id AND
                    items.id = ?"""

    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, item_name, description, status, classes, edit_time):
    sql = """UPDATE items SET   item_name = ?,
                                description = ?,
                                status = ?,
                                edit_time = ?
                        WHERE   id = ?
                        """
    db.execute(sql, [item_name, description, status, edit_time, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql="INSERT INTO item_classes (item_id, item_class_name, value) VALUES (?, ?, ?)"
    for item_class_name, value in classes:
        db.execute(sql, [item_id, item_class_name, value])
    return

def remove_item(item_id):
    sql = "DELETE FROM images WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    return db.execute(sql, [item_id])

def find_item(query, status, location):
    sql = """
        SELECT DISTINCT items.id, items.item_name, items.status
        FROM items
        LEFT JOIN item_classes ON items.id = item_classes.item_id
        WHERE 1=1
    """
    parameters = []

    if query:
        sql += " AND (items.item_name LIKE ? OR items.description LIKE ?)"
        parameters += ["%" + query + "%", "%" + query + "%"]

    if status:
        sql += " AND items.status = ?"
        parameters.append(status)

    if location:
        sql += " AND item_classes.item_class_name = 'Where' AND item_classes.value = ?"
        parameters.append(location)

    sql += " ORDER BY items.id DESC"

    return db.query(sql, parameters)

def get_all_classes():
    sql = "SELECT class_name, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for class_name, value in result:
        classes[class_name] = []
    for class_name, value in result:
        classes[class_name].append(value)

    return classes

def get_classes(item_id):
    sql = "SELECT item_class_name, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id = ?"
    result = db.query(sql, [item_id])
    return result

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def add_image(item_id, image, edit_time):
    sql = "INSERT INTO images (item_id, image) VALUES(?, ?)"
    db.execute(sql, [item_id, image])

    sql = "UPDATE items SET edit_time = ? WHERE id = ?"
    return db.execute(sql, [edit_time, item_id])

def remove_image(image_id, item_id, edit_time):
    sql = "DELETE FROM images WHERE id = ?"
    db.execute(sql, [image_id])

    sql = "UPDATE items SET edit_time = ? WHERE id = ?"
    return db.execute(sql, [edit_time, item_id])