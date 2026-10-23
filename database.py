
import sqlite3

connection = sqlite3.connect("onboardops.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")

connection.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_client_title
    ON tasks (client, title)
""")

connection.commit()
connection.close()
