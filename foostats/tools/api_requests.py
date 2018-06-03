"""
The tools that allow to communicate with google sheets through API.
"""
import os
import httplib2

from googleapiclient.discovery import build as build_service
from oauth2client import (
    client as oauth_client,
    file as oauth_file,
    tools as oauth_tools,
)

from foostats.settings import CREDENTIALS_FOLDER


def get_api_service():
    """
    Sets up a connection with google APIs and returns service variable
    which is used for sending requests.
    """
    scopes = 'https://www.googleapis.com/auth/spreadsheets'
    credentials_file = os.path.join(CREDENTIALS_FOLDER, 'credentials.json')
    store = oauth_file.Storage(credentials_file)
    creds = store.get()

    if not creds or creds.invalid:
        client_file = os.path.join(CREDENTIALS_FOLDER, 'client_secret.json')
        flow = oauth_client.flow_from_clientsecrets(
            client_file, scopes)
        creds = oauth_tools.run_flow(flow, store)

    service = build_service(
        'sheets', 'v4', http=creds.authorize(httplib2.Http()))
    return service
