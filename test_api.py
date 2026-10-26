def test_get_tasks_returns_client_tasks(api_client):
    api_client.post("/tasks", json={"client": "Acme", "title": "Create account"})

    response = api_client.get("/clients/Acme/tasks")

    assert response.status_code == 200
    assert response.json()["client"] == "Acme"
    assert response.json()["tasks"] == [
        {"id": 1, "title": "Create account", "status": "pending", "due_date": None}
    ]


def test_create_task_uses_default_status_and_validates_input(api_client):
    response = api_client.post(
        "/tasks", json={"client": "Acme", "title": "Create account"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "client": "Acme",
        "title": "Create account",
        "status": "pending",
        "due_date": None,
    }
    assert api_client.post("/tasks", json={"client": "Acme"}).status_code == 422


def test_update_task_returns_success_or_not_found(api_client):
    api_client.post("/tasks", json={"client": "Acme", "title": "Create account"})

    updated = api_client.patch(
        "/clients/Acme/tasks/Create account", json={"status": "completed"}
    )
    missing = api_client.patch(
        "/clients/Acme/tasks/Missing", json={"status": "completed"}
    )

    assert updated.status_code == 200
    assert updated.json() == {"updated": True}
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Task not found"}
    assert (
        api_client.patch("/clients/Acme/tasks/Create account", json={}).status_code
        == 422
    )


def test_delete_task_returns_success_or_not_found(api_client):
    api_client.post("/tasks", json={"client": "Acme", "title": "Create account"})

    deleted = api_client.delete("/clients/Acme/tasks/Create account")
    missing = api_client.delete("/clients/Acme/tasks/Create account")

    assert deleted.status_code == 200
    assert deleted.json() == {"deleted": True}
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Task not found"}


def test_onboarding_endpoint_creates_tasks_and_preserves_completed_status(api_client):
    created = api_client.post("/clients/Acme/onboarding")

    assert created.status_code == 200
    assert {(task["title"], task["status"]) for task in created.json()} == {
        ("Create account", "pending"),
        ("Configure integration", "pending"),
        ("Complete onboarding", "pending"),
    }

    api_client.patch("/clients/Acme/tasks/Create account", json={"status": "completed"})
    repeated = api_client.post("/clients/Acme/onboarding")

    assert repeated.status_code == 200
    assert len(repeated.json()) == 3
    assert (
        next(task for task in repeated.json() if task["title"] == "Create account")[
            "status"
        ]
        == "completed"
    )


def test_get_clients_empty(api_client):
    response = api_client.get("/clients")
    assert response.status_code == 200
    assert response.json() == {"clients": []}


def test_get_clients_with_one_client(api_client):
    api_client.post(
        "/tasks",
        json={"client": "Netflix", "title": "Create account", "status": "pending"},
    )
    response = api_client.get("/clients")
    assert response.json() == {
        "clients": [{"name": "Netflix", "progress_percent": 0.0}]
    }


def test_get_clients_with_multiple_clients(api_client):
    api_client.post(
        "/tasks",
        json={
            "client": "Netflix",
            "title": "Create account",
            "status": "pending",
        },
    )

    api_client.post(
        "/tasks",
        json={
            "client": "Google",
            "title": "Configure integration",
            "status": "completed",
        },
    )

    response = api_client.get("/clients")

    assert response.status_code == 200
    # Write an assertion checking the complete JSON response.
    assert response.json() == {
        "clients": [
            {"name": "Google", "progress_percent": 100.0},
            {"name": "Netflix", "progress_percent": 0.0},
        ]
    }


def test_get_clients_without_duplicate_names(api_client):
    api_client.post(
        "/tasks",
        json={
            "client": "Netflix",
            "title": "Create account",
            "status": "completed",
        },
    )

    api_client.post(
        "/tasks",
        json={
            "client": "Netflix",
            "title": "Configure integration",
            "status": "pending",
        },
    )

    response = api_client.get("/clients")

    assert response.status_code == 200
    assert response.json() == {
        "clients": [{"name": "Netflix", "progress_percent": 50.0}]
    }


def test_task_deadline_is_saved(api_client):
    response = api_client.post(
        "/tasks",
        json={
            "client": "Netflix",
            "title": "Configure integration",
            "status": "pending",
            "due_date": "2026-11-05",
        },
    )
    assert response.status_code == 200
    response = api_client.get("/clients/Netflix/tasks")
    assert response.status_code == 200
    task = response.json()["tasks"][0]["due_date"]
    assert task == "2026-11-05"


def test_task_without_deadline(api_client):
    response = api_client.post(
        "/tasks",
        json={
            "client": "Netflix",
            "title": "Create account",
            "status": "pending",
        },
    )
    response = api_client.get("/clients/Netflix/tasks")

    assert response.status_code == 200

    saved_due_date = response.json()["tasks"][0]["due_date"]
    assert saved_due_date is None
