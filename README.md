# CLI Budget Tracker Application

## Brief Description
The CLI Budget Tracker Application is a command-line interface tool designed to help small business users users manage their budget effectively. It allows users to track income and expenses, categorize transactions, and generate financial reports. The application supports multiple accounts and categories, making it suitable for both personal and small business use.

## Get Started
1. **Clone the repository:**
    ```
    git clone <repository-url>
    cd cli-budget-tracker-app
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    Create a [.env] file in the root directory and add the following:
    ```env
    BUDG_DATA_PATH=<path-to-data-directory>
    ```

4. **Run the application:**
    ```
    python main.py
    ```

## Technologies Used
- **Python**: The main programming language used for the application.
- **colorama**: For colored terminal text.
- **termcolor**: For additional text coloring options.
- **art**: For ASCII art generation.
- **python-dotenv**: For managing environment variables.
- **inquirer**: For interactive command-line prompts.
- **yaspin**: For terminal spinners.
- **pyfiglet**: For generating ASCII text banners.
- **tabulate2**: For creating formatted tables.

## Attributes
- **Accounts**: Manage multiple accounts such as checking, savings, and credit cards.
- **Categories**: Categorize transactions into predefined or custom categories.
- **Entries**: Add, view, search, and delete income and expense entries.
- **Reports**: Generate financial reports based on custom parameters like date range, category, and account.
- **Validation**: Ensure data integrity with input validation for dates, amounts, and other fields.
- **Interactive CLI**: User-friendly command-line interface with prompts and menus.