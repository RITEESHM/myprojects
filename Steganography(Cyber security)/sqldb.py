import sqlite3

def view_users(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    db_name = "user.db"
    users = view_users(db_name)
    for user in users:
        print(user)
