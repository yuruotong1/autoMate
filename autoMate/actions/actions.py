from utils.models import session, LLMApi, Task
from utils.code_utils import run_task
from datetime import datetime, timezone

def config_LLM():
    '''
        See a list of existing LLM configurations
        Delete old ones or add new config
    '''
    llm_configs = session.query(LLMApi).all()
    while True:
        print("\n--- LLM Configurations ---")
        if not llm_configs:
            print("No LLM configurations found.")
        else:
            for i, config in enumerate(llm_configs, 1):
                print(f"{i}. {config}")

        print("\nOptions:")
        print("1. Add new LLM configuration")
        print("2. Delete an LLM configuration")
        print("3. Back to main menu")

        choice = input("Select an option: ")

        if choice == '1':
            new_config = input("Enter new LLM configuration: ")
            llm_configs.append(new_config)
            print(f"Added new LLM configuration: {new_config}")
        elif choice == '2':
            if not llm_configs:
                print("No configurations to delete.")
            else:
                delete_index = int(input(f"Enter the number of the configuration to delete (1-{len(llm_configs)}): "))
                if 1 <= delete_index <= len(llm_configs):
                    removed = llm_configs.pop(delete_index - 1)
                    print(f"Deleted LLM configuration: {removed}")
                else:
                    print("Invalid selection.")
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")


def new_task():
    '''
    Chat with PM agent, enter name, description of the desired task
    '''
    pass

def see_existing_tasks():
    '''
    See a list of existing tasks, option to run one or delete it
    '''
    while True:
        print("\n--- Existing Tasks ---")
        tasks = session.query(Task).all()
        
        if not tasks:
            print("No tasks available.")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"task id: {task.id} - {task.name}: {task.description}")
                print(f"Last run at: {task.last_run_at}\n")

        print("\nOptions:")
        print("1. Run a task")
        print("2. Delete a task")
        print("3. Back to main menu")

        choice = input("Select an option: ")

        if choice == '1':
            if not tasks:
                print("No tasks to run.")
            else:
                run_index = int(input(f"Enter the id of the task to run: "))
                if run_index in [task.id for task in tasks]: # collect all task ids
                    run_task(run_index)
                else:
                    print("Invalid selection.")
        elif choice == '2':
            if not tasks:
                print("No tasks to delete.")
            else:
                delete_index = int(input(f"Enter the id of the task to delete: "))
                if delete_index in [task.id for task in tasks]:
                    removed = session.get(Task, delete_index)
                    session.delete(removed)
                    session.commit()
                    print(f"Deleted task: {removed.name}")
                else:
                    print("Invalid selection.")
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")