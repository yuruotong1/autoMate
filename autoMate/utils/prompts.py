'''
TODO:
Prompts for different tasks to be performed by the agent
1. A product manager to talk with the user, identify their true needs, identify if the need is
sutable for programs. Split the task, no need to write code, but rather THINK as a programmer
for the user, because the user doesn't know how to achieve their goal with code.
2. (Possibly) An architect, further split the overall task into lesser chunks, ideally so small
  the programmer agents cannot make mistakes
3. Finally, programmer agents to implement the tasks
Programmer agents should be given necessary infomation about the users' system, and 
  be able to directly manipulate the working directory, with shell commands or python,
  create the virtual environment, install the dependencies...
'''

import string

test_prompt= string.Template('''
    This is just a test run, reply shortly to save tokens.
                             ''')