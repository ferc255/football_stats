"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials_write.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1DB814bM2tHdwsCDdaQK05ER8GPkpzaUc8xhfO9aAGIE'
RANGE_NAME = 'Common!A1:C2'
'''
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])
for item1 in values:
    print(item1)
'''
values = [
    ['A', 'B', 'C'],
    ['A', 'B', 'C'],
]
body = {
    'values': values
}
body2 = {
    'properties': {
        'title': 'new_sheet',
    },
}
body3 = {
    'requests': {
        'addSheet': {
            'properties': {
                'title': 'new_sheet',
            },
        },
    }
}

#body4 = json.load('body4.json')
#body4 = json.loads(open('body4.json').read().format(sourceSheetId=SPREADSHEET_ID))
body4 = open('body4.json').read()

body4 = body4# % ((355237090,) * 2)

body4 = json.loads(body4)




request = service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body=body4).execute()
print(request)


'''
value_input_option = "RAW"
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
    valueInputOption=value_input_option, body=body).execute()
print('{0} cells updated.'.format(result.get('updatedCells')));
'''

#print(values)
'''
if not values:
    print('No data found.')
else:
    print('Name, Major:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))
'''
