#Flask web app with MySQL Integration


This Flask-based web application allows users to manage trainer details through a MySQL database. It provides functionalities to create new trainer records, view existing records, and edit trainer information.

## Prerequisites
- Python 3.x
- Flask
- Flask-MySQLdb

## Setup
1. Install dependencies: `pip install Flask Flask-MySQLdb`
2. Set up MySQL database configuration in `app.py`.
3. Run the application: `python app.py`

## Files
- `app.py`: Contains the main Flask application with routes for managing trainer data.
- `display_trainer.html`: Template for displaying trainer details.
- `trainer_details.html`: Form for adding new trainer records.

## Usage
- Access the home page at `/` to navigate to different sections.
- Create new trainer records at `/trainer` and view all records at `/trainer_data`.

Feel free to customize the database configuration and application logic based on your requirements.
