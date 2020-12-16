from googleapiclient.discovery import build
import urllib.request
import json

print("Please enter your youtube channel ID")
name = input()  # 輸入頻道的id


def total_view_time(name):  # 輸入頻道ID獲取該頻道的總觀看次數
    key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" +
        name +
        "&key=" +
        key).read()  # 讀取資料
    total_view = json.loads(data)['items'][0]['statistics']['viewCount']
    print("You have %d" % int(total_view) + "total view")

def total_subscribers(name):  # 輸入頻道ID獲取該頻道的總訂閱數
    key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" +
        name +
        "&key=" +
        key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    print("You have %d" % int(subs) + " subscribers")


def channel_description(name):  # 輸入頻道ID獲取頻道簡介
    api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
    youtube = build('youtube', 'v3', developerKey=api_key)
    res = youtube.channels().list(
        id=name,
        part='brandingSettings').execute()
    description = res['items'][0]['brandingSettings']['channel']['description']
    print(description)

def Playlists_Count(name):  # 輸入頻道ID獲取頻道中總共的播放清單數量
    content = youtube_api.playlists().list(channelId=channelid,
                                           part='snippet').execute()
    playlist_count = content['pageInfo']['totalResults']
    return playlist_count

total_view_time(name)
total_subscribers(name)
channel_description(name)

