from utils.models import session, LLMApi, Task
from utils.code_utils import run_task
from utils.openai_utils import chat
from utils.logging_utils import logger
from datetime import datetime, timezone
from agents.manager_agent import manager_agent

def config_LLM():
    '''
        See a list of existing LLM configurations
        Delete old ones or add new config
    '''
    llms = session.query(LLMApi).all()
    while True:
        print("\n--- LLM Configurations ---")
        if not llms:
            print("No LLM configurations found.")
        else:
            for llm in llms:
                print(f"LLM id: {llm.id} - {llm.name} ... {"Active" if llm.is_active else "Inactive"}")
                print(f"Last used at: {llm.last_used_at}\n")

        print("\nOptions:")
        print("1. Add new LLM configuration")
        print("2. Delete an LLM configuration")
        print("3. Toggle LLM active/inactive")
        print("4. Back to main menu")

        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter name for new LLM configuration: ")
            api_key = input("Paste your API KEY here: ")
            base_url = input("Paste your LLM provider's request url")
            new_config = LLMApi(name=name, _api_key=api_key, base_url=base_url)
            session.add(new_config)
            session.commit()
            print(f"Added new LLM configuration: {name}")
        elif choice == '2':
            if not llms:
                print("No configurations to delete.")
            else:
                delete_index = int(input(f"Enter the number of the configuration to delete: "))
                if delete_index in [llm.id for llm in llms]:
                    removed = session.get(LLMApi, delete_index)
                    session.delete(removed)
                    session.commit()
                    print(f"Deleted configuration: {removed.name}")
                else:
                    print("Invalid selection.")
        elif choice == '3':
            # TODO: I'll do this when we have users.
            print("Coming later, delete the LLM configuration for now.")
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")


def new_task():
    '''
    Chat with PM agent, enter name, description of the desired task
    '''
    tasks = session.query(Task).all()
    existing_task_names = [task.name for task in tasks]
    llms = session.query(LLMApi).all()
    active_llms = [llm for llm in llms if llm.is_active]
    first_activate_llm = active_llms[0]
    while True:
        if not first_activate_llm:
            print("Please add a LLM configuration first. ")
            break
        task_name = input("Enter a name for this task: ") # TODO: check for unique
        description = input("What would you like to do? \n")
        llm_response = chat(first_activate_llm, manager_agent, starter=description)
        print(llm_response)
        manager_agent.listen(llm_response)

        break

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
            for task in tasks:
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