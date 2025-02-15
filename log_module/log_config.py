import logging
import logging.config
import os


def setup_logging(logging_base_dir=None):
    logging_base_dir=logging_base_dir if logging_base_dir else os.path.join(os.getcwd(),'log')
    if not os.path.exists(logging_base_dir): 
        os.makedirs(logging_base_dir) 
    """
    Setup application logging
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Set log level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
        filename=os.path.join(logging_base_dir,'application.log')
    )