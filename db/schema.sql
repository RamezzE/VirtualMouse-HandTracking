CREATE TABLE IF NOT EXISTS Actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Mappings (
    gesture_id INTEGER KEY UNIQUE NOT NULL,
    action_id INTEGER NOT NULL,
	PRIMARY KEY (gesture_id, action_id),
    FOREIGN KEY(action_id) REFERENCES Actions(id)
);

CREATE TABLE IF NOT EXISTS CameraSettings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DetectionSettings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS MouseSettings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
);