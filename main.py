
from onboarding import show_onboarding

from storage import (
    save_task,
    get_tasks,
    update_status_task
)


client_names = ["Acme", "Microsoft"]

for client_name in client_names:
    tasks = show_onboarding(client_name)

    for task in tasks:
        save_task(task)


updated = update_status_task(
    "Apple",
    "Configure integration",
    "completed"
)

if updated:
    print("Success!")
else:
    print("Task not found!")


print(get_tasks("Acme"))
