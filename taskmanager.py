#this is task management system, data is stored in json file. so,  data remains persistent.
import json
from datetime import datetime

#this function will return highest task id+1 and this will be used to add new task
def get_task_id():
    try:
        with open('taskfile.json', 'r') as file:
            json_data = [json.loads(line) for line in file]
            task_ids = [data['taskid'] for data in json_data]
            if len(task_ids) == 0:
                return 1
            else:
                return max(task_ids) + 1
    except FileNotFoundError:
        return 1

#this function will add task, will ask for task details, priority and due date.
def add_task():
    task = input("Enter task details: ")
    priority = input("Enter task priority (High/Medium/Low): ").lower()
    due_date = input("Enter due date (YYYY-MM-DD): ")

    if task.strip() == '' or priority not in ['high', 'medium', 'low'] or not due_date:
        print('Invalid input. Task not added. Please try again.')
    else:
        try:
            with open('taskfile.json', 'a') as file:
                task_id = get_task_id()
                #creating  a dictionary to dump as json
                task_to_add = {
                    'taskid': task_id,
                    'task': task,
                    'status': '',
                    'priority': priority,
                    'due_date': due_date
                }
                json_object = json.dumps(task_to_add)
                file.write(json_object + '\n')
            print('Task added successfully!')
        except Exception as e:
            print(f"Error adding task: {e}")
#function for viewing tasks 
def view_tasks():
    try:
        with open('taskfile.json', 'r') as file:
            json_data = [json.loads(line) for line in file]
            print('{:<10}{:<20}{:<10}{:<15}{:>5}'.format('Task ID', 'Task', 'Priority', 'Due Date', 'Status'))
            for data in json_data:
                task_id = str(data.get('taskid', ''))
                task = data.get('task', '')
                priority = str(data.get('priority', ''))
                due_date = data.get('due_date', '')
                status = data.get('status', '')
                print('{:<10}{:<20}{:<10}{:<15}{:>5}'.format(task_id, task, priority, due_date, status))
    except FileNotFoundError:
        print('No tasks found.')
    except Exception as e:
        print(f"Error viewing tasks: {e}")
#function to mark a task as completed, this takes task_id as input
def mark_task_completed(task_id):
    try:
        with open('taskfile.json', 'r') as file:
            json_data = [json.loads(line) for line in file]
        with open('taskfile.json', 'w') as file:
            for data in json_data:
                if data['taskid'] == task_id:
                    data['status'] = 'completed'
                json_object = json.dumps(data)
                file.write(json_object + '\n')
        print(f'Task {task_id} marked as completed.')
    except FileNotFoundError:
        print('No tasks found.')
    except Exception as e:
        print(f"Error marking task as completed: {e}")
#this is used to delete tasks and it takes task id as input
def delete_task(task_id):
    try:
        with open('taskfile.json', 'r') as file:
            json_data = [json.loads(line) for line in file]
            task_ids = [data['taskid'] for data in json_data]
            if task_id not in task_ids:
                print(f'There exists no task with ID {task_id}.')
            else:
                with open('taskfile.json', 'w') as file:
                    for data in json_data:
                        if data['taskid'] != task_id:
                            json_object = json.dumps(data)
                            file.write(json_object + '\n')
                    print(f'Task {task_id} deleted successfully.')
    except FileNotFoundError:
        print('No tasks found.')
    except Exception as e:
        print(f"Error deleting task: {e}")
#this function allows you to search tasks on the basis of either status, due date or priority
def search_tasks():
    try:
        with open('taskfile.json', 'r') as file:
            json_data = [json.loads(line) for line in file]

        search_option = input("Choose search option.\n1. Search by Status\n2. Search by Due Date\n3. Search by Priority\nEnter Number:")

        if search_option.strip() == "1":
            search_value = input("Enter status to search: ")
            search_field = 'status'
        elif search_option.strip() == "2":
            search_value = input("Enter due date to search (YYYY-MM-DD): ")
            search_field = 'due_date'
        elif search_option.strip() == "3":
            search_value = input("Enter priority to search (High/Medium/Low): ").lower()
            search_field = 'priority'
        else:
            print('Invalid search option. Please choose a valid option.')
            return

        matching_tasks = [data for data in json_data if data.get(search_field) == search_value]

        if not matching_tasks:
            print(f'No tasks found with {search_field} equal to {search_value}.')
        else:
            print('{:<10}{:<20}{:<10}{:<15}{:>5}'.format('Task ID', 'Task', 'Priority', 'Due Date', 'Status'))
            for data in matching_tasks:
                task_id = str(data.get('taskid', ''))
                task = data.get('task', '')
                priority = str(data.get('priority', ''))
                due_date = data.get('due_date', '')
                status = data.get('status', '')
                print('{:<10}{:<20}{:<10}{:<15}{:>5}'.format(task_id, task, priority, due_date, status))

    except FileNotFoundError:
        print('No tasks found.')
    except Exception as e:
        print(f"Error searching tasks: {e}")

while True:
    option = input("Choose an option.\n1. Add a Task\n2. View tasks\n3. Search tasks\n4. Mark a task completed\n5. Delete a task\n6. Exit\nEnter Number:")

    if option.strip() == "1":
        add_task()
    elif option.strip() == "2":
        view_tasks()
    elif option.strip() == "3":
        search_tasks()
    elif option.strip() == "4":
        task_id = int(input("Enter the task ID to mark as completed: "))
        mark_task_completed(task_id)
    elif option.strip() == "5":
        task_id = int(input("Enter the task ID to delete: "))
        delete_task(task_id)
    elif option.strip() == "6":
        break
    else:
        print('You entered an incorrect number. Kindly choose one of the numbers from 1 to 6.')
