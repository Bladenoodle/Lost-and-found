from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user(user_id):
    sql = "SELECT   id, username FROM users WHERE id = ?"

    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = "SELECT id, item_name, status FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        return None

    user = result[0]
    user_id = user["id"]
    password_hash = user["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None
