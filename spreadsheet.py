import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Membership Sign-in").get_worksheet(0)
transactions = client.open("USIT Membership Payment Confirmation 2018-2019").get_worksheet(0)
