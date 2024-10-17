import os
import json
from .models import Task, session

def create_task(task_name, entry_point_content, interval=-1):
    """
    Creates a new task with the given name and entry point content, 
    initializing a workspace and log file path.
    
    Args:
        task_name (str): The name of the task.
        entry_point_content (str): The Python code content for the task's main entry point.
        interval (int): Interval for task scheduling. Default is -1 for immediate tasks.
        
    Returns:
        int or None: The ID of the created task, or None if creation failed.
    """
    # Define workspace and log file paths
    workspace_dir = f'workspaces/{task_name}'
    entry_point_path = os.path.join(workspace_dir, 'main.py')
    log_file_path = os.path.join(workspace_dir, 'task.log')

    try:
        # Create the workspace directory if it does not exist
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)
        else:
            print(f"Workspace directory '{workspace_dir}' already exists. Files may be overwritten.")

        # Write the entry point content to the main.py file in the workspace
        with open(entry_point_path, 'w') as file:
            file.write(entry_point_content)

        # Create a new Task entry in the database
        task = Task(
            name=task_name,
            workspace_dir=workspace_dir,
            code_entry_point=entry_point_path,
            interval=interval,
            status="idle",
            log_file=log_file_path,
        )
        session.add(task)
        session.commit()

        print(f"Task '{task_name}' created successfully with ID {task.id} and workspace at '{workspace_dir}'.")
        return task.id

    except OSError as e:
        print(f"Failed to create workspace or write entry point for task '{task_name}': {e}")
        return None  # Return None on failure for consistency

    except Exception as e:
        session.rollback()  # Rollback in case of any database failure
        print(f"Failed to create task '{task_name}': {e}")
        return None  # Return None on failure for consistency
