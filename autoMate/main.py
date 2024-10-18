import signal
import sys
from actions.actions import *

def quit_program(signal_received=None, frame=None):
    print("\nExiting the program.")
    sys.exit(0)

COMMAND_MAP = {
    '1': config_LLM,
    '2': new_task,
    '3': see_existing_tasks,
    '4': quit_program
}

def main():

    signal.signal(signal.SIGINT, quit_program)

    while True:
        print("\nWelcome to autoMate:")
        print("1. View and edit LLM configurations.")
        print("2. Talk to agents to generate a new task.")
        print("3. View, edit, and run existing tasks.")
        print("4. Exit the program.\n")

        choice = input("Select an option: ")

        command = COMMAND_MAP.get(choice)
        if command:
            command()
        else:
            print("Invalid option. Please try again.")




if __name__ == "__main__":
    main()