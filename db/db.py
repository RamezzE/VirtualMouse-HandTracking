import sqlite3
import threading

class Database:
    _instance = None
    _lock = threading.Lock()  # Ensure thread-safe singleton creation

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path, schema_path):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.db_path = db_path
        self.schema_path = schema_path
        self.local = threading.local()
        self.is_updated = False
        self._create_tables_from_file(schema_path)
        self._check_and_insert_defaults()

        self._initialized = True

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

    def _check_and_insert_defaults(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        tables = tables[1:]

        all_tables_empty = True

        for table in tables:
            if not self._is_table_empty(table[0]):
                all_tables_empty = False
                break

        if all_tables_empty:
            self._insert_defaults()

    def _is_table_empty(self, table_name):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
        return count == 0

    def get_action_names(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM Actions")
        return [row[0] for row in c.fetchall()]

    def insert(self, table, **kwargs):
        conn = self._get_connection()
        c = conn.cursor()
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' * len(kwargs))
        values = tuple(kwargs.values())
        c.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        conn.commit()

    def get_all(self, table):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        return c.fetchall()

    def get(self, table, columns_to_select="*", **kwargs):
        conn = self._get_connection()
        c = conn.cursor()

        if isinstance(columns_to_select, list):
            columns_to_select = ', '.join(columns_to_select)
        else:
            columns_to_select = str(columns_to_select)

        where_clause = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
        values = tuple(kwargs.values())

        if not where_clause:
            query = f"SELECT {columns_to_select} FROM {table}"
            c.execute(query)
            return c.fetchall()

        query = f"SELECT {columns_to_select} FROM {table} WHERE {where_clause}"
        c.execute(query, values)

        return c.fetchone()

    def update(self, table, columns_to_update, **kwargs):
        conn = self._get_connection()
        c = conn.cursor()

        set_clause = ', '.join([f"{col} = ?" for col in columns_to_update.keys()])
        set_values = tuple(columns_to_update.values())

        where_clause = ' AND '.join([f"{key} = ?" for key in kwargs.keys()])
        where_values = tuple(kwargs.values())

        values = set_values + where_values

        c.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}", values)
        conn.commit()

    def delete_table_contents(self, table):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(f"DELETE FROM {table}")
        conn.commit()

    def drop_table(self, table):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(f"DROP TABLE {table}")
        conn.commit()

    def drop_all_tables(self):
        print('Dropping all tables')
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        tables = tables[1:]

        for table in tables:
            print(f'Dropped: {table[0]}')
            self.drop_table(table[0])

    def reset(self):
        self.drop_all_tables()
        self._create_tables_from_file(self.schema_path)
        self._check_and_insert_defaults()

    def _insert_defaults(self):

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

        actions = ['Idle',
                   'Drag',
                   'Move Mouse',
                   'Right Click',
                   'Left Click',
                   'Double Click',
                   'Zoom',
                   'Scroll Up',
                   'Scroll Down',
                   'Toggle Relative Mouse']

        dict = {
            INDEX: 'Drag',
            INDEX_MIDDLE: 'Move Mouse',
            INDEX_THUMB: 'Right Click',
            INDEX_MIDDLE_THUMB: 'Left Click',
            PEACE: 'Double Click',
            HAND_OPEN: 'Idle',
            FIST: 'Idle',
            PINCH: 'Zoom',
            THUMBS_UP: 'Scroll Up',
            THUMBS_DOWN: 'Scroll Down',
            THUMBS_PINKY: 'Toggle Relative Mouse'
        }

        print('\nInserting actions:\n')
        for action in actions:
            self.insert('Actions', name=action)
            print("Inserting: ", action)

        print('\nInserting mappings:\n')
        for key, value in dict.items():
            print(f'Inserting: {key} -> {value} (id: {self.get("Actions", columns_to_select="id", name=value)[0]})')
            self.insert('Mappings', gesture_id=key, action_id=self.get('Actions', columns_to_select='id', name=value)[0])

        print('\nInserting settings:\n')

        self.insert("CameraSettings", name="Camera", value=0)
        self.insert("CameraSettings", name="Show FPS", value=1)

        self.insert("DetectionSettings", name="Detection Confidence", value=0.5)
        self.insert("DetectionSettings", name="Tracking Confidence", value=0.5)
        self.insert("DetectionSettings", name="Detection Responsiveness", value = 3)

        print('Inserted everything\n')

    def close(self):
        if hasattr(self.local, 'connection'):
            self.local.connection.close()

if __name__ == '__main__':
    db = Database('db/actions.db', 'db/schema.sql')
    db.reset()
    db.close()
