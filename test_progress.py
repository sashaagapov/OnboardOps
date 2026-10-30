from onboarding import get_onboarding_progress
from storage import save_task


def add_task(client, title, status="pending"):
    save_task({"client": client, "title": title, "status": status})


def test_progress_is_zero_when_client_has_no_tasks(initialized_database):
    assert get_onboarding_progress("Unknown") == {
        "client": "Unknown",
        "total_tasks": 0,
        "completed_tasks": 0,
        "progress_percent": 0.0,
    }


def test_progress_is_33_33_for_one_completed_task_out_of_three(initialized_database):
    for title, status in [
        ("Create account", "completed"),
        ("Configure integration", "pending"),
        ("Complete onboarding", "pending"),
    ]:
        add_task("Netflix", title, status)

    assert get_onboarding_progress("Netflix") == {
        "client": "Netflix",
        "total_tasks": 3,
        "completed_tasks": 1,
        "progress_percent": 33.33,
    }


def test_progress_is_100_when_all_tasks_are_completed(initialized_database):
    add_task("Acme", "Create account", "completed")
    add_task("Acme", "Configure integration", "completed")

    progress = get_onboarding_progress("Acme")

    assert progress["total_tasks"] == 2
    assert progress["completed_tasks"] == 2
    assert progress["progress_percent"] == 100.0


def test_progress_counts_mixed_task_statuses(initialized_database):
    for title, status in [
        ("Create account", "completed"),
        ("Configure integration", "pending"),
        ("Complete onboarding", "completed"),
        ("Send welcome email", "in_progress"),
    ]:
        add_task("Acme", title, status)

    assert get_onboarding_progress("Acme")["progress_percent"] == 50.0


def test_progress_is_isolated_between_clients(initialized_database):
    add_task("Acme", "Create account", "completed")
    add_task("Netflix", "Create account", "pending")
    add_task("Netflix", "Configure integration", "pending")

    assert get_onboarding_progress("Acme")["progress_percent"] == 100.0
    assert get_onboarding_progress("Netflix")["progress_percent"] == 0.0


def test_progress_endpoint_returns_the_progress_json(api_client):
    api_client.post("/clients/Netflix/onboarding")
    api_client.patch(
        "/clients/Netflix/tasks/Create account", json={"status": "completed"}
    )

    response = api_client.get("/clients/Netflix/progress")

    assert response.status_code == 200
    assert response.json() == {
        "client": "Netflix",
        "total_tasks": 3,
        "completed_tasks": 1,
        "progress_percent": 33.33,
    }
