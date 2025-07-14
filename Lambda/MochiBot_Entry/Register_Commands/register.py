import os
import requests
import json

APP_ID = os.environ["DISC_APP_ID"]
GUILD_ID = os.environ["DISC_GUILD_ID"]
BOT_TOKEN = os.environ["DISC_BOT_TOKEN"]

url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

commandData = {
    "name": "foo",
    "description": "replies with bar ;/",
}

response = requests.post(url, headers=headers, data=json.dumps(commandData))

print(f"Status Code: {response.status_code}")
print(response.json())