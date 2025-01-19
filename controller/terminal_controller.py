from colorama import init
from termcolor import colored
import art

def print_welcome_screen():
    init()
    applicaiton_name=art.text2art('Budget Tracker App')
    version="0.1"
    describtion='Welcome to budger tracker app, your comprehensive budget tracking application to help mange your small business manage finances across multiple accounts, categories, and time periods.'
    print(colored(applicaiton_name, 'green'))
    print(colored(f'version {version}','red'))
    print(colored(describtion,'light_magenta'))
def main_menu():
    while True:
        menu_message="""
Select from the menu:
q- quit
"""
        menu_choice=input(menu_message)
        match menu_choice:
            case _:
                break