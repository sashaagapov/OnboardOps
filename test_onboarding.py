from onboarding import show_onboarding


EXPECTED_TITLES = [
    "Create account",
    "Configure integration",
    "Complete onboarding",
]


def test_onboarding_generates_three_predefined_pending_tasks():
    tasks = show_onboarding("Netflix")

    assert tasks == [
        {"client": "Netflix", "title": title, "status": "pending"}
        for title in EXPECTED_TITLES
    ]


def test_onboarding_results_are_independent_for_different_clients():
    first_client_tasks = show_onboarding("Netflix")
    second_client_tasks = show_onboarding("Acme")

    first_client_tasks[0]["status"] = "completed"

    assert {task["client"] for task in second_client_tasks} == {"Acme"}
    assert all(task["status"] == "pending" for task in second_client_tasks)
