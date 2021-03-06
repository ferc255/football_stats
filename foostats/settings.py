"""
Settings of the application. Contains important constants.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_DIR = os.path.join(
    os.path.expanduser('~'),
    'app_credentials/google_api/'
)

MAXIMUM_CELL_BRIGHTNESS = 0.4

MIN_MATCH_COUNT = 10

SOURCE_SPREADSHEET_ID = '1QH-AFYHk3lXJf-dG3FzhDwtO6iJZus7ZXWoY8aBs7ZI'
SPREADSHEET_ID = '1DB814bM2tHdwsCDdaQK05ER8GPkpzaUc8xhfO9aAGIE'
