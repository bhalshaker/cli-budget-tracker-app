from controller import terminal,data
import time
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    data_base_dir= os.getenv('BUDG_DATA_PATH') if os.getenv('BUDG_DATA_PATH') else os.getcwd()
    data.DataController.create_all_none_created_csv(data_base_dir)
    data.DataController.load_data_from_files(data_base_dir)
    terminal.TerminalController.print_welcome_screen()
    time.sleep(3)
    terminal.TerminalController.main_menu()
    data.DataController.save_data_to_files(data_base_dir)
if __name__=="__main__":
    main()