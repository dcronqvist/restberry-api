import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import config as config

SCOPES = [
	"https://www.googleapis.com/auth/drive",
	"https://www.googleapis.com/auth/drive.readonly",
	"https://www.googleapis.com/auth/drive.file",
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/spreadsheets.readonly"
]

secret_file = config.get_setting("secret_file")

def refresh_token():
	creds = None
	if os.path.exists("token.pickle"):
		with open("token.pickle", "rb") as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
			creds = flow.run_local_server(port=25455)
		with open("token.pickle", "wb") as token:
			pickle.dump(creds, token)
	print("Refresh Google API.")
	return build("sheets", "v4", credentials=creds)

def set_values(service, id, cell, value):
	sheet = service.spreadsheets()
	body = { "values": [[value]] }
	result = sheet.values().update(spreadsheetId=id, range=cell, valueInputOption="USER_ENTERED", body=body).execute()
	if result:
		return True
	else:
		return False

def get_values(service, id, range, rvo):
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=id, range=range, valueRenderOption=rvo).execute()
	values = result.get("values", [])
	return values

def get_row_from_first_c(rows, key):
	for row in rows:
		if len(row) > 0:
			if row[0] == key:
				return row
	return None

def register_outcome(date, category, description, amount):
	sheet = config.get_setting("economy-out-form")
	url = f"https://docs.google.com/forms/d/e/{sheet}/formResponse?usp=pp_url&entry.2084142997={date}&entry.1064711960={category}&entry.1493521456={description}&entry.199758250={amount}&submit=Submit"
	resp = requests.get(url)
	if resp:
		return True
	return False

def register_income(date, category, description, amount):
	sheet = config.get_setting("economy-in-form")
	url = f"https://docs.google.com/forms/d/e/{sheet}/formResponse?usp=pp_url&entry.1885435352={date}&entry.218079050={category}&entry.1056613280={amount}&entry.316191158={description}&submit=Submit"
	resp = requests.get(url)
	if resp:
		return True
	return False
