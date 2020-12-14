from datetime import datetime
from googleapiclient.discovery import build
print("Please enter your channel ID")
channel_id = input()  # 輸入頻道ID
api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
youtube = build('youtube', 'v3', developerKey=api_key)
res = youtube.channels().list(
    id=channel_id,
    part='brandingSettings').execute()
description = res['items'][0]['brandingSettings']['channel']['description']
print(description)