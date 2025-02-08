import re
from inquirer import errors
from controller.data import DataController

class TerminalValidationController():

    def amount_validation(answers, current):
        if not re.match(r"\d{1,}|(\d{1,}.\d{1,3})", current):
            raise errors.ValidationError("", reason="Not a valid amount")
        return True
    
    def validate_date(answers, current):
        try:
            DataController.convert_string_to_date(current)
            return True
        except ValueError:
            raise errors.ValidationError('', reason='Invalid date format. Please use MM-DD-YYYY.')

    def validate_date_range(answers, current):
        if TerminalValidationController.validate_date(answers, current):
            start_date = DataController.convert_string_to_date(answers['start_date'])
            end_date = DataController.convert_string_to_date(current)
            if end_date >= start_date:
                raise errors.ValidationError('', reason='End date must be after or equal to start date')
        return True
        
    def validate_type(answers, current):
        if current.upper() not in ["I","INCOME","E","EXPENSE"]:
            raise errors.ValidationError('',reason='Please enter a valid budget item type i for income and e for expense')
        
    def validate_account(answers,current):
        if DataController.does_account_exist(current):
            raise errors.ValidationError('',reason='This account already exists')
        return True
    
    def validate_category(answers,current):
        if DataController.does_category_exist(current):
            raise errors.ValidationError('',reason='This category already exists')
        return True
    
    def validate_year(answers,current):
        check_date=f'01-01-{current}'
        try:
            DataController.convert_string_to_date(check_date)
            return True 
        except:
            errors.ValidationError('',reason='Year should be in the following format YYYY')
