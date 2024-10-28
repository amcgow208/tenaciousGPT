import sqlite3

class UserDatabase:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_users_table()
        self.create_chat_history_table()

    def create_users_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS USERS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL UNIQUE,
        PASSWORD TEXT NOT NULL);
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        self.conn.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def validate_user(self, username, password):
        cursor = self.conn.execute("SELECT * FROM USERS WHERE USERNAME=? AND PASSWORD=?", (username, password))
        return cursor.fetchone() is not None

    def create_chat_history_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS CHAT_HISTORY
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID INTEGER NOT NULL,
            MESSAGE TEXT NOT NULL,
            SENDER TEXT NOT NULL,
            TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID));
            ''')
        self.conn.commit()

    def add_chat_message(self, user_id, message, sender):
        self.conn.execute("INSERT INTO CHAT_HISTORY (USER_ID, MESSAGE, SENDER) VALUES (?, ?, ?)",
                          (user_id, message, sender))
        self.conn.commit()

    def get_chat_history(self, user_id):
        cursor = self.conn.execute("SELECT MESSAGE, SENDER FROM CHAT_HISTORY WHERE USER_ID=? ORDER BY TIMESTAMP ASC",
                                   (user_id,))
        return cursor.fetchall()

    def get_user_id(self, username):
        cursor = self.conn.execute("SELECT ID FROM USERS WHERE USERNAME=?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_user_chat_sessions(self, username):
        user_id = self.get_user_id(username)
        if user_id is None:
            return []
        return [{'session_id': user_id, 'session_name': f'Chat with {username}'}]

    def close(self):
        self.conn.close()


