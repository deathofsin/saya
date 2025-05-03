from config import FOUNDER
import sqlite3

def is_admin(user_id):
    if not isinstance(user_id, int):
        return False

    conn = sqlite3.connect("database/admin.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM admins WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    return row is not None or user_id == FOUNDER