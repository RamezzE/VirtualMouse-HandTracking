import sqlite3

FIST_CLOSED = 0
HAND_OPEN = 1
INDEX_MIDDLE_THUMB_EXTENDED = 2
INDEX_THUMB_EXTENDED = 3
INDEX_MIDDLE_EXTENDED = 4
INDEX_EXTENDED = 5
PINCH = 6
THUMB_EXTENDED = 7
SCISSORS = 8


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
            'idle': 0,
            'left click': 1,
            'right click': 2,
            'move mouse': 3,
            'drag': 4,
            'pinch': 5,
            'scroll': 6,
            'double click': 7
        }
        
        arr = ['idle', 'left click', 'right click', 'move mouse', 'drag', 'pinch', 'scroll', 'double click']
        
        for action in arr:
            self.insertAction(action)
        
        self.insertMapping(gesture_id = FIST_CLOSED, action_id = actions['idle'] + 1)
        self.insertMapping(gesture_id = HAND_OPEN, action_id = actions['idle'] + 1)
        self.insertMapping(gesture_id = INDEX_EXTENDED, action_id = actions['drag'] + 1)
        self.insertMapping(gesture_id = INDEX_MIDDLE_EXTENDED, action_id = actions['move mouse'] + 1)
        self.insertMapping(gesture_id = INDEX_MIDDLE_THUMB_EXTENDED, action_id = actions['left click'] + 1)
        self.insertMapping(gesture_id = INDEX_THUMB_EXTENDED, action_id = actions['right click'] + 1)
        self.insertMapping(gesture_id = PINCH, action_id = actions['pinch'] + 1)
        self.insertMapping(gesture_id = SCISSORS, action_id = actions['double click'] + 1)
        self.insertMapping(gesture_id = THUMB_EXTENDED, action_id = actions['scroll'] + 1)
        

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
        
    print(db.getActionNames())
    
    print(db.getMappings())
    # print(db.getMappings()[0][1])
    db.close()
