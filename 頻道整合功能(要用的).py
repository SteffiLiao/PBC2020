from googleapiclient.discovery import build
import urllib.request
import json
import sys
website_link = input()
if website_link[0:26] == "https://www.youtube.com/c/":  # 若連結為該形式，告訴使用者輸入錯誤
    print("Sorry,we can't find channel id through this link.")
    sys.exit()
if website_link[0:29] == "https://www.youtube.com/user/":
    print("Sorry,we can't find channel id through this link.")
    sys.exit()
else:
    wanted_channel_id = website_link[32:]
    print(wanted_channel_id)
    api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(
        id=wanted_channel_id,
        part='contentDetails').execute()


def total_view_time(wanted_channel_id):  # 輸入頻道ID獲取該頻道的總觀看次數
    key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" +
        wanted_channel_id +
        "&key=" +
        key).read()  # 讀取資料
    total_view = json.loads(data)['items'][0]['statistics']['viewCount']
    print("You have %d" % int(total_view) + " total view")

def total_subscribers(wanted_channel_id):  # 輸入頻道ID獲取該頻道的總訂閱數
    key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" +
        wanted_channel_id +
        "&key=" +
        key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    print("You have %d" % int(subs) + " subscribers")


def channel_description(wanted_channel_id):  # 輸入頻道ID獲取頻道簡介
    api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(
        id=wanted_channel_id,
        part='brandingSettings').execute()
    description = res['items'][0]['brandingSettings']['channel']['description']
    print(description)

total_view_time(wanted_channel_id)
total_subscribers(wanted_channel_id)
channel_description(wanted_channel_id)

