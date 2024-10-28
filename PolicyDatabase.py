import sqlite3
import json

class PolicyDatabase:
    def __init__(self, db_name='policy_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS POLICIES
        (ID TEXT PRIMARY KEY,
        TITLE TEXT NOT NULL,
        CONTENT TEXT NOT NULL);
        ''')
        self.conn.commit()

    def import_from_json(self, *json_file_paths):
        for json_file_path in json_file_paths:  # Iterate over each file path
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for category in data['categories']:  # Access the categories key
                    for policy in category['policies']:  # Iterate through each policy in the category
                        self.add_policy(policy['id'], policy['title'], policy['content'])

    def add_policy(self, policy_id, title, content):
        try:
            self.conn.execute("INSERT OR REPLACE INTO POLICIES (ID, TITLE, CONTENT) VALUES (?, ?, ?)",
                              (policy_id, title, content))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while adding policy to the database: {e}")

    def search_policies(self, search_query):
        print(f"Searching for: {search_query}")  # Debug output
        cursor = self.conn.execute("SELECT * FROM POLICIES WHERE TITLE LIKE ? OR CONTENT LIKE ?",
                                   ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        print(f"Found {len(results)} results")  # Debug output
        return results

    def get_policy_by_id(self, policy_id):
        cursor = self.conn.execute("SELECT * FROM POLICIES WHERE ID = ?", (policy_id,))
        result = cursor.fetchone()
        return result

    def close(self):
        self.conn.close()
