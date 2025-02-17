import sqlite3


class DatabaseApp:
    def __init__(self, db_name="test.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """
        )
        self.conn.commit()

    def insert_user(self, name, email):
        try:
            self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def update_user(self, user_id, name, email):
        self.cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseApp()
    user_id = db.insert_user("John Doe", "john@example.com")
    print(f"Inserted User ID: {user_id}")
    print("All Users:", db.get_all_users())
    print("Search User:", db.get_user_by_email("john@example.com"))
    db.update_user(user_id, "John Updated", "john_updated@example.com")
    print("After Update:", db.get_all_users())
    db.delete_user(user_id)
    print("After Deletion:", db.get_all_users())
    db.close()