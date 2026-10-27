import sqlite3


def init_db():
    connection = sqlite3.connect("onboardops.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT
        )
    """)

    columns = connection.execute("PRAGMA table_info(tasks)").fetchall()

    column_names = []

    for column in columns:
        column_names.append(column[1])

    if "due_date" not in column_names:
        connection.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

    connection.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_client_title
        ON tasks (client, title)
    """)

    connection.commit()
    connection.close()

