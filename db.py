import sqlite3
import threading

INDEX = 0
INDEX_MIDDLE = 1
INDEX_THUMB = 2
INDEX_MIDDLE_THUMB = 3
PEACE = 4
HAND_OPEN = 5
FIST = 6
PINCH = 7
THUMBS_UP = 8
THUMBS_DOWN = 9
THUMBS_PINKY = 10

class Database:
    def __init__(self, db_path, schema_path):
        self.db_path = db_path
        self.schema_path = schema_path
        self.local = threading.local()
        self.is_updated = False
        self._create_tables_from_file(schema_path)

    def _get_connection(self):
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path)
        return self.local.connection

    def _create_tables_from_file(self, schema_path):
        conn = self._get_connection()
        c = conn.cursor()
        with open(schema_path, 'r') as f:
            sql_script = f.read()
        c.executescript(sql_script)
        conn.commit()

    def insert_action(self, name):
        conn = self._get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Actions (name) VALUES (?)", (name,))
            conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            print("Action already exists.")
            return self.get_action_id(name)

    def get_action_names(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM Actions")
        return [row[0] for row in c.fetchall()]

    def insert_mapping(self, gesture_id, action_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Mappings WHERE gesture_id = ? AND action_id = ?", (gesture_id, action_id))
        if c.fetchone():
            print("Mapping already exists.")
            return False
        else:
            c.execute("INSERT INTO Mappings (action_id, gesture_id) VALUES (?, ?)", (action_id, gesture_id))
            conn.commit()
            return True

    def insert_mappings(self, mappings):
        for i in range(len(mappings)):
            self.insert_mapping(i, mappings[i])

    def get_mappings(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT gesture_id, action_id FROM Mappings")
        return c.fetchall()

    def get_action_by_gesture_id(self, gesture_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('''
            SELECT a.name
            FROM Actions a
            JOIN Mappings m ON a.id = m.action_id
            WHERE m.gesture_id = ?
        ''', (gesture_id,))
        result = c.fetchone()
        return result[0] if result else None

    def delete_actions(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Actions")
        conn.commit()

    def reset(self):
        self.delete_mappings()
        self.delete_actions()
        self.drop_tables()
        self._create_tables_from_file(self.schema_path)
        self.insert_defaults()

    def insert_defaults(self):
        actions = {
            'Idle': 0,
            'Move Mouse': 1,
            'Left Click': 2,
            'Double Click': 3,
            'Drag': 4,
            'Right Click': 5,
            'Scroll Up': 6,
            'Scroll Down': 7,
            'Zoom': 8,
            'Toggle Relative Mouse': 9,
        }

        arr = [
            'Idle',
            'Move Mouse',
            'Left Click',
            'Double Click',
            'Drag',
            'Right Click',
            'Pinch',
            'Scroll Up',
            'Scroll Down',
            'Zoom',
            'Toggle Relative Mouse'
        ]

        for action in arr:
            self.insert_action(action)

        self.insert_mapping(gesture_id=INDEX, action_id=actions['Drag'])
        self.insert_mapping(gesture_id=INDEX_MIDDLE, action_id=actions['Move Mouse'])
        self.insert_mapping(gesture_id=INDEX_THUMB, action_id=actions['Right Click'])
        self.insert_mapping(gesture_id=INDEX_MIDDLE_THUMB, action_id=actions['Left Click'])
        self.insert_mapping(gesture_id=PEACE, action_id=actions['Double Click'])
        self.insert_mapping(gesture_id=HAND_OPEN, action_id=actions['Idle'])
        self.insert_mapping(gesture_id=FIST, action_id=actions['Idle'])
        self.insert_mapping(gesture_id=PINCH, action_id=actions['Zoom'])
        self.insert_mapping(gesture_id=THUMBS_UP, action_id=actions['Scroll Up'])
        self.insert_mapping(gesture_id=THUMBS_DOWN, action_id=actions['Scroll Down'])
        self.insert_mapping(gesture_id=THUMBS_PINKY, action_id=actions['Toggle Relative Mouse'])

    def delete_mappings(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Mappings")
        conn.commit()

    def drop_tables(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DROP TABLE Actions")
        c.execute("DROP TABLE Mappings")
        conn.commit()

    def close(self):
        if hasattr(self.local, 'connection'):
            self.local.connection.close()

if __name__ == '__main__':
    db = Database('db/actions.db', 'db/schema.sql')
    db.reset()

    print(db.get_mappings())
    print(db.get_mappings()[0][1])
    db.close()
