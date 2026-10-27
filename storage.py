import sqlite3


def save_task(task):
    connection = sqlite3.connect("onboardops.db")

    result = connection.execute(
        """
        INSERT INTO tasks (client, title, status, due_date)
        VALUES (?, ?, ?,?)
        ON CONFLICT(client, title) DO NOTHING
        """,
        (task["client"], task["title"], task["status"],task.get("due_date"),)
    )

    connection.commit()
    connection.close()
    return result.rowcount == 1


def get_tasks(client_name):
    connection = sqlite3.connect("onboardops.db")

    rows = connection.execute(
        "SELECT id, title, status, due_date FROM tasks WHERE client = ?", (client_name,)
    ).fetchall()

    formatted_tasks = []

    for row in rows:
        task = {"id": row[0], "title": row[1], "status": row[2], "due_date": row[3]}
        formatted_tasks.append(task)

    connection.close()
    return formatted_tasks


def update_status_task(client_name, title, new_status):
    connection = sqlite3.connect("onboardops.db")

    result = connection.execute(
        "UPDATE tasks SET status = ? WHERE client = ? AND title = ?",
        (new_status, client_name, title),
    )

    connection.commit()
    connection.close()

    return result.rowcount == 1


def delete_task(client_name, title):

    connection = sqlite3.connect("onboardops.db")

    result = connection.execute(
        "DELETE FROM tasks WHERE client = ? AND title = ? ", (client_name, title)
    )
    connection.commit()
    connection.close()
    return result.rowcount == 1

def get_clients():
    connection = sqlite3.connect("onboardops.db")

    rows = connection.execute("SELECT DISTINCT client FROM tasks ORDER BY client").fetchall()
    clients = []
    for row in rows:
        clients.append(row[0])

    connection.close()
    return clients
