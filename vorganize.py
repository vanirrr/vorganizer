## Time organizing program

import json
import os

DATA_FILE = "data.json"

def load_data():
    # Load datafile / handle corruption
    if not os.path.exists(DATA_FILE):
        data = {"timetable": {}, "progress": {}}
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r") as df:
            return json.load(df)
    except (json.JSONDecodeError, ValueError):
        try:
            backup_name = DATA_FILE + ".bak"
            os.replace(DATA_FILE, backup_name)
        except Exception:
            pass
        data = {"timetable": {}, "progress": {}}
        save_data(data)
        return data
    
def save_data(data):
    with open(DATA_FILE, "w") as df:
        json.dump(data, df, indent=4)

def create_module(data, category):
    if "categories" not in data:
        data["categories"] = []
    data["categories"].append(category)
    save_data(data)
    print("Created category: ", category)

def add_task(data, day, module, task):
    if day not in data["timetable"]:
        data["timetable"][day] = {}
    if module not in data["timetable"][day]:
        data["timetable"][day][module] = []
    data["timetable"][day][module].append(task)
    save_data(data)
    print("Added task: ", task)

def mark_task_complete(data, module, task):
    if module not in data["progress"]:
        data["progress"][module] = []
    data["progress"][module].append(task)
    save_data(data)
    print("Task marked complete!")

def view_timetable(data):
    for day, modules in data["timetable"].items():
        print(f"Day: {day}")
        for module, tasks in modules.items():
            print(f"  Module: {module}")
            for idx, task in enumerate(tasks, start=1):
                status = "✓" if module in data["progress"] and task in data["progress"][module] else "✗"
                print(f"    {idx}. [{status}] {task}")

def remove_task(data, day, module, task):
    if day in data["timetable"] and module in data["timetable"][day]:
        if task in data["timetable"][day][module]:
            data["timetable"][day][module].remove(task)
            save_data(data)
            print("Removed task: ", task)
        else:
            print("Task not found.")
    else:
        print("Day or module not found.")
def edit_task(data, day, module, old_task, new_task):
    if day in data["timetable"] and module in data["timetable"][day]:
        if old_task in data["timetable"][day][module]:
            index = data["timetable"][day][module].index(old_task)
            data["timetable"][day][module][index] = new_task
            save_data(data)
            print("Edited task: ", old_task, " to ", new_task)
        else:
            print("Old task not found.")
    else:
        print("Day or module not found.")

def main():
    data = load_data()
    while True:
        print("\nOptions:")
        print("1. Create Category")
        print("2. Add Task")
        print("3. Mark Task Complete")
        print("4. View Timetable")
        print("5. Remove Task")
        print("6. Edit Task")
        print("7. Exit")

        choice = input("Choose an option: ")
        
        if choice == "1":
            category = input("Enter category name: ")
            create_module(data, category)
        elif choice == "2":
            day = input("Enter day (e.g., Monday): ")
            module = input("Enter module name: ")
            task = input("Enter task description: ")
            add_task(data, day, module, task)
        elif choice == "3":
            # Select day
            if not data.get("timetable"):
                print("No tasks scheduled.")
                continue
            days = list(data["timetable"].keys())
            for i, d in enumerate(days, start=1):
                print(f"{i}. {d}")
            try:
                day_sel = int(input("Choose a day number (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if day_sel == 0:
                continue
            if not (1 <= day_sel <= len(days)):
                print("Day number out of range.")
                continue
            selected_day = days[day_sel - 1]

            # Select module
            modules = list(data["timetable"][selected_day].keys())
            for i, m in enumerate(modules, start=1):
                print(f"{i}. {m}")
            try:
                mod_sel = int(input("Choose a module number (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if mod_sel == 0:
                continue
            if not (1 <= mod_sel <= len(modules)):
                print("Module number out of range.")
                continue
            selected_module = modules[mod_sel - 1]

            # Select task by number
            tasks = data["timetable"][selected_day][selected_module]
            if not tasks:
                print("No tasks in that module.")
                continue
            for i, t in enumerate(tasks, start=1):
                status = "✓" if selected_module in data["progress"] and t in data["progress"][selected_module] else "✗"
                print(f"{i}. [{status}] {t}")
            try:
                task_sel = int(input("Choose task number to mark complete (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if task_sel == 0:
                continue
            if not (1 <= task_sel <= len(tasks)):
                print("Task number out of range.")
                continue
            selected_task = tasks[task_sel - 1]
            mark_task_complete(data, selected_module, selected_task)
        elif choice == "4":
            view_timetable(data)
        elif choice == "5":
            day = input("Enter day (e.g., Monday): ")
            module = input("Enter module name: ")
            task = input("Enter task description to remove: ")
            remove_task(data, day, module, task)
        elif choice == "6":
            # Choosing day number from the timetable like other functions
            print("Select day to edit task:")
            if not data.get("timetable"):
                print("No tasks scheduled.")
                continue
            days = list(data["timetable"].keys())
            for i, d in enumerate(days, start=1):
                print(f"{i}. {d}")
            try:                day_sel = int(input("Choose a day number (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if day_sel == 0:
                continue
            if not (1 <= day_sel <= len(days)):
                print("Day number out of range.")
                continue
            selected_day = days[day_sel - 1]
            # Select module
            modules = list(data["timetable"][selected_day].keys())
            for i, m in enumerate(modules, start=1):
                print(f"{i}. {m}")
            try:
                mod_sel = int(input("Choose a module number (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if mod_sel == 0:
                continue
            if not (1 <= mod_sel <= len(modules)):
                print("Module number out of range.")
                continue
            selected_module = modules[mod_sel - 1]
            # Select task to edit
            tasks = data["timetable"][selected_day][selected_module]
            if not tasks:
                print("No tasks in that module.")
                continue
            for i, t in enumerate(tasks, start=1):
                print(f"{i}. {t}")
            try:
                task_sel = int(input("Choose task number to edit (or 0 to cancel): "))
            except ValueError:
                print("Invalid input.")
                continue
            if task_sel == 0:
                continue
            if not (1 <= task_sel <= len(tasks)):
                print("Task number out of range.")
                continue
            selected_task = tasks[task_sel - 1]
            new_task = input("Enter new task description: ")
            edit_task(data, selected_day, selected_module, selected_task, new_task)
            break
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
