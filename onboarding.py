from storage import get_tasks


def get_onboarding_progress(client_name):
    tasks = get_tasks(client_name)

    total_tasks = len(tasks)
    completed_tasks = 0
    for task in tasks:
        if task["status"] == "completed":
            completed_tasks += 1

    if total_tasks > 0:
        progress_percent = round(completed_tasks * 100 / total_tasks, 2)
    else:
        progress_percent = 0.0

    return {
        "client": client_name,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percent": progress_percent,
    }


def show_onboarding(client_name):
    print(f"Onboarding for {client_name}:")

    task_titles = ["Create account", "Configure integration", "Complete onboarding"]

    tasks = []

    for title in task_titles:
        task = {"title": title, "status": "pending", "client": client_name}

        tasks.append(task)

    return tasks
