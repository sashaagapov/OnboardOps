import sqlite3

from storage import delete_task, get_tasks, save_task, update_status_task


def task(client="Acme", title="Configure integration", status="pending"):
    return {"client": client, "title": title, "status": status}


def test_database_initialization_creates_tasks_schema(initialized_database):
    with sqlite3.connect("onboardops.db") as connection:
        columns = [row[1] for row in connection.execute("PRAGMA table_info(tasks)")]
        indexes = [row[1] for row in connection.execute("PRAGMA index_list(tasks)")]

    assert columns == ["id", "client", "title", "status"]
    assert "idx_tasks_client_title" in indexes


def test_save_and_retrieve_multiple_tasks_for_client(initialized_database):
    save_task(task(title="Create account"))
    save_task(task(title="Complete onboarding", status="completed"))

    saved_tasks = get_tasks("Acme")

    assert {(item["title"], item["status"]) for item in saved_tasks} == {
        ("Create account", "pending"),
        ("Complete onboarding", "completed"),
    }


def test_duplicate_task_is_not_inserted_or_overwritten(initialized_database):
    save_task(task(status="completed"))
    save_task(task(status="pending"))

    saved_tasks = get_tasks("Acme")

    assert len(saved_tasks) == 1
    assert saved_tasks[0]["status"] == "completed"


def test_clients_can_have_tasks_with_same_title(initialized_database):
    save_task(task(client="Acme"))
    save_task(task(client="Netflix"))

    assert len(get_tasks("Acme")) == 1
    assert len(get_tasks("Netflix")) == 1


def test_unknown_client_has_no_tasks(initialized_database):
    assert get_tasks("Unknown") == []


def test_update_changes_only_the_matching_task(initialized_database):
    save_task(task(client="Acme"))
    save_task(task(client="Netflix"))

    assert update_status_task("Acme", "Configure integration", "completed") is True
    assert get_tasks("Acme")[0]["status"] == "completed"
    assert get_tasks("Netflix")[0]["status"] == "pending"
    assert update_status_task("Acme", "Missing task", "completed") is False


def test_delete_removes_only_the_matching_task(initialized_database):
    save_task(task(client="Acme"))
    save_task(task(client="Netflix"))

    assert delete_task("Acme", "Configure integration") is True
    assert get_tasks("Acme") == []
    assert len(get_tasks("Netflix")) == 1
    assert delete_task("Acme", "Configure integration") is False
