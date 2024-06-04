import sqlite3

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
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.__create_tables_from_file(schema_path)

    def __create_tables_from_file(self, schema_path):
        with open(schema_path, 'r') as f:
            sql_script = f.read()
        self.c.executescript(sql_script)
        self.conn.commit()

    def insertAction(self, name):
        try:
            self.c.execute("INSERT INTO Actions (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.c.lastrowid
        except sqlite3.IntegrityError:
            print("Action already exists.")
            return self.get_action_id(name)
        
    def getActionNames(self):
        self.c.execute("SELECT name FROM Actions")
        return [row[0] for row in self.c.fetchall()]
        
    def insertMapping(self, gesture_id, action_id):
        self.c.execute("SELECT * FROM Mappings WHERE gesture_id = ? AND action_id = ?", (gesture_id, action_id))
        if self.c.fetchone():
            print("Mapping already exists.")
            return False
        else:
            self.c.execute("INSERT INTO Mappings (action_id, gesture_id) VALUES (?, ?)", (action_id, gesture_id))
            self.conn.commit()
            return True

    def getMappings(self):
        self.c.execute("SELECT gesture_id, action_id FROM Mappings")
        return self.c.fetchall()
    
    def get_action_by_gesture_id(self, gesture_id):
        self.c.execute('''
            SELECT a.name
            FROM Actions a
            JOIN Mappings m ON a.id = m.action_id
            WHERE m.gesture_id = ?
        ''', (gesture_id,))
        result = self.c.fetchone()
        return result[0] if result else None

    def deleteActions(self):
        self.c.execute("DELETE FROM Actions")
        self.conn.commit()
        
    def reset(self):
        self.deleteMappings()
        self.deleteActions()
        
        self.dropTables()
        self.__init__(self.db_path, self.schema_path)
        
        self.insertDefaults()
        
    def insertDefaults(self):
        actions = {
            'Idle': 0,
            'Move Mouse': 1,
            'Left Click': 2,
            'Double Click': 3,
            'Drag': 4,
            'Right Click': 5,
            'Scroll Up': 6,
            'Scroll Down': 7,
            'Zoom' : 8,
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
            self.insertAction(action)

        self.insertMapping(gesture_id = INDEX, action_id = actions['Drag'])
        self.insertMapping(gesture_id = INDEX_MIDDLE, action_id = actions['Move Mouse'])
        self.insertMapping(gesture_id = INDEX_THUMB, action_id = actions['Right Click'])
        self.insertMapping(gesture_id = INDEX_MIDDLE_THUMB, action_id = actions['Left Click'])
        self.insertMapping(gesture_id = PEACE, action_id = actions['Double Click'])
        self.insertMapping(gesture_id = HAND_OPEN, action_id = actions['Idle'])
        self.insertMapping(gesture_id = FIST, action_id = actions['Idle'])
        self.insertMapping(gesture_id = PINCH, action_id = actions['Zoom'])
        self.insertMapping(gesture_id = THUMBS_UP, action_id = actions['Scroll Up'])
        self.insertMapping(gesture_id = THUMBS_DOWN, action_id = actions['Scroll Down'])
        self.insertMapping(gesture_id = THUMBS_PINKY, action_id = actions['Toggle Relative Mouse'])

    def deleteMappings(self):
        self.c.execute("DELETE FROM Mappings")
        self.conn.commit()
        
    def dropTables(self):
        self.c.execute("DROP TABLE Actions")
        self.c.execute("DROP TABLE Mappings")
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database('db/actions.db', 'db/schema.sql')
    db.reset()
    
    print(db.getMappings())
    print(db.getMappings()[0][1])
    db.close()
