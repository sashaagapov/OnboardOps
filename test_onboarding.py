from onboarding import show_onboarding


def test_onboarding_creates_three_tasks():
    tasks = show_onboarding("Netflix")
    assert len(tasks) == 3


def test_check_if_pending():
    tasks = show_onboarding("Netflix")
    for task in tasks:
        assert task["status"] == "pending"
