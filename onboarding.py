
def show_onboarding(client_name):
    print(f"Onboarding for {client_name}:")

    task_titles = [
        "Create account",
        "Configure integration",
        "Complete onboarding"
    ]

    tasks = []

    for title in task_titles:
        task = {
            "title": title,
            "status": "pending",
            "client": client_name
        }

        tasks.append(task)

    return tasks
