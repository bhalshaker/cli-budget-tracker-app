from controller import terminal,data
import time
import os
from dotenv import load_dotenv

def initiliaze_env():
    """
    This method initializes the environment variables.
    """
    load_dotenv()
    data.DataController.data_base_dir= os.getenv('BUDG_DATA_PATH') if os.getenv('BUDG_DATA_PATH') else os.getcwd()


def main():
    """
    This is the main method of the program.
    """
    initiliaze_env()
    data.DataController.create_all_none_created_csv()
    data.DataController.load_data_from_files()
    terminal.TerminalController.print_welcome_screen()
    terminal.TerminalController.main_menu()
if __name__=="__main__":
    main()