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

SPREADSHEET_ID = '1DB814bM2tHdwsCDdaQK05ER8GPkpzaUc8xhfO9aAGIE'
