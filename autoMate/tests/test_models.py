import unittest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.models import Base, LLMApi, Task 

# Set up a test database in memory
TEST_DATABASE_URL = 'sqlite:///:memory:'

class TestDatabaseModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize a new engine and session for testing
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        
    def setUp(self):
        # Begin a new session and initialize data
        self.session = self.Session()
    
    def tearDown(self):
        # Rollback any changes to the session and close it
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        # Dispose of the engine and drop all tables
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()
    
    def test_create_llm_api(self):
        # Test creating an LLMApi record
        llm_api = LLMApi(name="TestAPI", _api_key="dummy_key", base_url="https://testapi.com")
        self.session.add(llm_api)
        self.session.commit()

        # Query and check if the record was added
        api = self.session.query(LLMApi).filter_by(name="TestAPI").one()
        self.assertEqual(api.name, "TestAPI")
        self.assertEqual(api._api_key, "dummy_key")
        self.assertEqual(api.base_url, "https://testapi.com")
        self.assertIsNotNone(api.created_at)
        self.assertTrue(api.is_active)
    
    def test_unique_constraint_on_llm_api_name(self):
        # Attempt to add two LLMApi records with the same name
        llm_api1 = LLMApi(name="DuplicateAPI", _api_key="dummy_key_1", base_url="https://testapi1.com")
        llm_api2 = LLMApi(name="DuplicateAPI", _api_key="dummy_key_2", base_url="https://testapi2.com")
        self.session.add(llm_api1)
        self.session.commit()

        # Adding the second with the same name should fail
        self.session.add(llm_api2)
        with self.assertRaises(Exception):
            self.session.commit()
            self.session.rollback()
    
    def test_create_task(self):
        # Test creating a Task record
        task = Task(
            name="TestTask",
            description="This is a test task",
            workspace_dir="/test/workspace",
            code_entry_point="/test/workspace/main.py",
            interval=15,
            log_file="/test/workspace/task.log"
        )
        self.session.add(task)
        self.session.commit()

        # Query and check if the record was added
        created_task = self.session.query(Task).filter_by(name="TestTask").one()
        self.assertEqual(created_task.name, "TestTask")
        self.assertEqual(created_task.description, "This is a test task")
        self.assertEqual(created_task.status, "idle")  # Default status
        self.assertEqual(created_task.interval, 15)
        self.assertTrue(created_task.is_attached)

    def test_default_values_in_task(self):
        # Test if default values are set correctly
        task = Task(
            name="DefaultValuesTask",
            workspace_dir="/default/dir",
            code_entry_point="/default/dir/main.py",
            interval=10,
        )
        self.session.add(task)
        self.session.commit()
        
        # Check the default values
        fetched_task = self.session.query(Task).filter_by(name="DefaultValuesTask").one()
        self.assertEqual(fetched_task.status, "idle")
        self.assertTrue(fetched_task.is_attached)
        self.assertIsNotNone(fetched_task.created_at)
        self.assertIsNone(fetched_task.last_run_at)

    def test_update_task_status(self):
        # Test updating a task's status
        task = Task(
            name="UpdateStatusTask",
            workspace_dir="/update/status/dir",
            code_entry_point="/update/status/dir/main.py",
            interval=5
        )
        self.session.add(task)
        self.session.commit()

        # Update the task status
        task.status = "failed"
        self.session.commit()
        
        # Retrieve and check the status
        updated_task = self.session.query(Task).filter_by(name="UpdateStatusTask").one()
        self.assertEqual(updated_task.status, "failed")
