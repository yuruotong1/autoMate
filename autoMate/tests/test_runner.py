import unittest
import os
import sys
from datetime import datetime, timezone

# Modify sys.path to import custom modules from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.code_utils import run_task
from utils.models import Task, session

class TestRunTask(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Define a test directory within the project folder
        cls.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cls.test_dir = os.path.join(cls.project_dir, 'test_tasks')
        os.makedirs(cls.test_dir, exist_ok=True)
        print(f"Test artifacts will be saved in: {cls.test_dir}")

    def setUp(self):
        # Start a new session for each test
        self.session = session

    def tearDown(self):
        # Roll back any database changes to maintain a clean state
        self.session.rollback()

    @classmethod
    def tearDownClass(cls):
        # Optionally inform that the artifacts are kept
        print(f"Test artifacts retained in directory: {cls.test_dir}")
        # Optionally, uncomment the following lines to clean up the directory after testing:
        # for root, dirs, files in os.walk(cls.test_dir, topdown=False):
        #     for name in files:
        #         os.remove(os.path.join(root, name))
        #     for name in dirs:
        #         os.rmdir(os.path.join(root, name))
        # os.rmdir(cls.test_dir)

    def create_test_task(self, task_name, main_content, additional_files=None):
        """
        Helper function to create a test task with given main.py content
        and additional files if any.
        """
        # Define paths
        workspace_dir = os.path.join(self.test_dir, task_name)
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Write main.py content
        main_file_path = os.path.join(workspace_dir, 'main.py')
        with open(main_file_path, 'w') as main_file:
            main_file.write(main_content)

        # Write additional files if provided
        if additional_files:
            for filename, content in additional_files.items():
                file_path = os.path.join(workspace_dir, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as file:
                    file.write(content)
        
        # Create a Task entry in the database
        task = Task(
            name=task_name,
            workspace_dir=workspace_dir,
            code_entry_point=main_file_path,
            log_file=os.path.join(workspace_dir, 'task.log'),
            interval=0,
            status="idle",
            is_attached=False
        )
        self.session.add(task)
        self.session.commit()
        
        return task

    def test_run_simple_main(self):
        # Simple main.py that prints a success message
        main_content = """
print("Task executed successfully")
"""
        task = self.create_test_task("SimpleTask", main_content)
        
        # Run the task
        result = run_task(task.id)
        
        # Read the log file and check for the expected output
        with open(task.log_file, 'r') as log:
            log_content = log.read()
        self.assertIn("Task executed successfully", log_content)

    def test_run_multi_file_task(self):
        # main.py imports and calls another function from an additional file
        main_content = """
from helper import greet
greet()
"""
        helper_content = """
def greet():
    print("Hello from the helper file!")
"""
        additional_files = {"helper.py": helper_content}
        task = self.create_test_task("MultiFileTask", main_content, additional_files)
        
        # Run the task
        result = run_task(task.id)
        
        # Read the log file and check for the expected output
        with open(task.log_file, 'r') as log:
            log_content = log.read()
        self.assertIn("Hello from the helper file!", log_content)

    def test_run_failing_task(self):
        # main.py with a runtime error
        main_content = """
print("Starting task")
raise Exception("Intentional Error")
"""
        task = self.create_test_task("FailingTask", main_content)
        
        # Run the task
        result = run_task(task.id)
        
        # Read the log file and check for the error message
        with open(task.log_file, 'r') as log:
            log_content = log.read()
        self.assertIn("Intentional Error", log_content)
        self.assertIn("Traceback", log_content)  # Check for the traceback presence

    def test_run_task_with_subdirectory(self):
        # main.py in a directory with other nested files and directories
        main_content = """
from utils.helper import assist
assist()
print("Main task complete")
"""
        helper_content = """
def assist():
    print("Assistance provided by helper.")
"""
        additional_files = {
            "utils/helper.py": helper_content
        }
        task = self.create_test_task("SubdirectoryTask", main_content, additional_files)
        
        # Run the task
        result = run_task(task.id)
        
        # Read the log file and check for the expected output
        with open(task.log_file, 'r') as log:
            log_content = log.read()
        self.assertIn("Assistance provided by helper.", log_content)
        self.assertIn("Main task complete", log_content)
