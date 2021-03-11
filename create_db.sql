-- SQLite
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
)