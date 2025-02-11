from controller.data import DataController
from controller.terminal import TerminalController
import time
import os
from dotenv import load_dotenv
from log_module import log_config
import logging

def initiliaze_env():
    """
    This method initializes the environment variables.
    """
    load_dotenv()
    DataController.data_base_dir= os.getenv('BUDG_DATA_PATH') if os.getenv('BUDG_DATA_PATH') else os.path.join(os.getcwd(),'data')
    log_config.setup_logging(os.getenv('LOGGING_DIR_PATH'))
    return logging.getLogger(__name__)


def main():
    """
    This is the main method of the program.
    """
    logger=initiliaze_env()
    logger.info('Bedget Application Tracker was just started ...')
    TerminalController.print_welcome_screen()
    logger=initiliaze_env()
    logger.info('configured data and logging location of directories')
    DataController.create_all_none_created_csv()
    DataController.load_data_from_files()
    TerminalController.main_menu()
    logger.info('Exited budget application tracker safely ...')
if __name__=="__main__":
    main()