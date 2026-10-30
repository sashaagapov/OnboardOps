import sqlite3
from datetime import date


def save_task(task):
    connection = sqlite3.connect("onboardops.db")

    result = connection.execute(
        """
        INSERT INTO tasks (client, title, status, due_date)
        VALUES (?, ?, ?,?)
        ON CONFLICT(client, title) DO NOTHING
        """,
        (
            task["client"],
            task["title"],
            task["status"],
            task.get("due_date"),
        ),
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

    rows = connection.execute(
        "SELECT DISTINCT client FROM tasks ORDER BY client"
    ).fetchall()
    clients = []
    for row in rows:
        clients.append(row[0])

    connection.close()
    return clients


def get_operations_summary():
    connection = sqlite3.connect("onboardops.db")
    all_tasks = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    completed_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'completed'"
    ).fetchone()[0]
    pending_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'pending'"
    ).fetchone()[0]
    in_progress_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'in_progress'"
    ).fetchone()[0]
    overdue_tasks = connection.execute(
        """
    SELECT COUNT(*) FROM tasks
    WHERE due_date < ? AND status IN ('pending', 'in_progress')
    """,
        (date.today().isoformat(),),
    ).fetchone()[0]
    unique_clients = connection.execute(
        "SELECT COUNT(DISTINCT client) FROM tasks "
    ).fetchone()[0]
    connection.close()
    if all_tasks == 0:
        completion_rate = 0.0
    else:
        completion_rate = round(completed_tasks / all_tasks * 100, 2)
    return {
        "total_tasks": all_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completion_rate": completion_rate,
        "overdue_tasks": overdue_tasks,
        "unique_clients": unique_clients,
    }
