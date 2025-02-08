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

3. **Set up environment variables (Optional otherwise base_directory/data is the default location):**
    Create a [.env] file in the root directory and add the following:
    ```env
    BUDG_DATA_PATH=<path-to-data-directory>
    ```

4. **Run the application:**
    ```
    python main.py
    ```

## Technologies Used
- **Python3.11+**: The main programming language used for the application.
- **colorama**: For colored terminal text.
- **termcolor**: For additional text coloring options.
- **python-dotenv**: For managing environment variables.
- **inquirer**: For interactive command-line prompts.
- **pyfiglet**: For generating ASCII text banners.

## Attributes
Does not apply