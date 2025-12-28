import flet as ft
import json
import os

def main(page: ft.Page):
    page.title = "VividTasks"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "tasks.json")
    print("Saving JSON to:", json_path)

    page.add(ft.Text("Select a task category", size=24, weight=ft.FontWeight.BOLD))

    task_options = ft.Dropdown(
        options=[
            ft.dropdown.Option("Work"),
            ft.dropdown.Option("Personal"),
            ft.dropdown.Option("Shopping"),
            ft.dropdown.Option("Others"),
        ],
        value="Work",
        width=900,
    )
    page.add(task_options)

    task_input = ft.TextField(hint_text="Add a new task", expand=True)
    add_button = ft.Button("Add Task")

    tasks_list = ft.Column(
        spacing=10,
        height=200,
        width=900,
        scroll=ft.ScrollMode.ALWAYS,
        auto_scroll=True,
        expand=True
    )

    def save_tasks(e=None):
        tasks = []
        for row in tasks_list.controls:
            checkbox = row.controls[0]
            text = row.controls[1]
            tasks.append({"label": text.value, "value": checkbox.value})

        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4, ensure_ascii=False)
            print("Saved tasks:", len(tasks))
        except Exception as ex:
            print("Error saving:", ex)

    def load_tasks():
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                print("Loaded tasks:", len(tasks))

                for task in tasks:
                    tasks_list.controls.append(
                        ft.Row(
                            [
                                ft.Checkbox(value=task.get("value", False)),
                                ft.Text(task.get("label", ""), no_wrap=False, expand=True)
                            ],
                            expand=True
                        )
                    )
            except Exception as ex:
                print("Error loading:", ex)
        else:
            print("No tasks.json found.")
        page.update()

    def add_task(e):
        task = task_input.value.strip()
        if task:
            tasks_list.controls.append(
                ft.Row(
                    [
                        ft.Checkbox(value=False),
                        ft.Text(f"{task} ({task_options.value})", no_wrap=False, expand=True)
                    ],
                    expand=True
                )
            )
            task_input.value = ""
            save_tasks()
        page.update()

    add_button.on_click = add_task

    page.add(
        ft.Row([task_input, add_button]),
        tasks_list
    )

    def delete_task(e):
        if tasks_list.controls:
            tasks_list.controls.pop()
            save_tasks()
        page.update()

    page.add(ft.Button("Delete Last Task", on_click=delete_task))

    def delete_all_tasks(e):
        tasks_list.controls.clear()
        save_tasks()
        page.update()

    def switch_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    page.add(ft.Button("Delete All Tasks", on_click=delete_all_tasks))
    page.add(ft.Button("Switch Theme", on_click=switch_theme))

    page.on_close = save_tasks

    load_tasks()
ft.run(main)