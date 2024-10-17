import subprocess
import traceback
import json
from .models import Task, session
from datetime import datetime, timezone

import json
import subprocess
from datetime import datetime, timezone

def run_task(task_id):
    '''
        Run an existing task based on the unique task_id
        An entrypoint is always a main.py file located at the root of task folder
        We prompt the coder agent to follow this convention
        Args:
            task_id (int): unique task_id stored in database
        Returns:
            result (JSON): if in attached mode, result will be given to coder agent for correction
                          if not, result will be given to UI
    '''
    task = session.get(Task, task_id)
    if not task:
        return json.dumps({'UI': 'Task not found'})

    if task.is_attached:
        return _run_attached_task(task)
    else:
        return _run_detached_task(task)


def _run_attached_task(task):
    entry_point = task.code_entry_point
    log_file = task.log_file

    try:
        with open(log_file, 'w') as log:
            result = subprocess.run(["python3", entry_point], stdout=log, stderr=log, text=True)

        task.status = "success" if result.returncode == 0 else "failed"
        task.last_run_at = datetime.now(timezone.utc)
        session.commit()

        if task.status == "failed":
            return json.dumps({'error': 'Task failed. Check log file for details.'})
        return json.dumps({'status': 'success'})

    except Exception as e:
        task.status = "failed"
        task.last_run_at = datetime.now(timezone.utc)
        session.commit()
        error_payload = {
            "error": {
                "type": e.__class__.__name__,
                "message": str(e),
                "direct_cause": str(e.__cause__) if e.__cause__ else None
            }
        }
        return json.dumps(error_payload)


def _run_detached_task(task):
    entry_point = task.code_entry_point
    log_file = task.log_file

    try:
        with open(log_file, 'w') as log:
            result = subprocess.run(["python3", entry_point], stdout=log, stderr=log, text=True)

        task.status = "success" if result.returncode == 0 else "failed"
        task.last_run_at = datetime.now(timezone.utc)
        session.commit()

        if task.status == "failed":
            print(f"Task '{task.name}' failed. Check the log file for details: {log_file}")
        else:
            print(f"Task '{task.name}' completed successfully.")

    except Exception as e:
        task.status = "failed"
        task.last_run_at = datetime.now(timezone.utc)
        session.commit()
        print(f"Failed to run task '{task.name}': {str(e)}")

