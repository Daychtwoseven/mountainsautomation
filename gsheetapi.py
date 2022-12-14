from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-7jFcNq6A9pruVeT7Jbe0kJTPrpzPx_MGC0TEam0xmE'


def main(city, values):
    try:
        print(values)
        if values:
            service = build('sheets', 'v4', credentials=creds)

            sheet = service.spreadsheets()
            body = {
                'values': values
            }
            print(f"{city}")
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A2:S2",
                                            valueInputOption="USER_ENTERED", body=body).execute()

    except HttpError as err:
        print(err)
