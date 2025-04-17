import db

def add_claim(item_id, user_id, contact_info):
    sql = "INSERT INTO claims (item_id, user_id, contact_info) VALUES (?, ?, ?)"
    return db.execute(sql, [item_id, user_id, contact_info])

def get_claims(item_id):
    sql = """SELECT claims.id, claims.contact_info, users.id AS user_id, users.username
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
    result = db.query(sql, [item_id, user_id])
    return result[0] if result else None

def remove_claim(claim_id):
    sql = "DELETE FROM claims WHERE id = ?"
    return db.execute(sql, [claim_id])

def replace_claim(claim_id, new_contact_info):
    sql = """UPDATE claims SET contact_info = ?
                           WHERE id = ?"""
    return db.execute(sql, [new_contact_info, claim_id])