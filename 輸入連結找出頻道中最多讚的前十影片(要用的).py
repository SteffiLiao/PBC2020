from datetime import datetime
from googleapiclient.discovery import build
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


def get_channel_videos(channel_id):  # 找出頻道的所有影片
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id,
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None  # 如果沒有下一頁(已找到最後一頁)

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos


videos = get_channel_videos(wanted_channel_id)
res = youtube.videos().list(
    id=videos[0]['snippet']['resourceId']['videoId'],
    part='statistics').execute()


def get_video_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(
            video_ids[i:i + 50]), part='snippet,contentDetails,statistics').execute()
        stats += res['items']
    return stats


video_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos))
stats = get_video_stats(video_ids)
count = 0
most_liked = sorted(
    stats,
    key=lambda x: int(
        x['statistics']['likeCount']),
    reverse=True)
temporary_list = []  # 暫存的列表
final_list = []
if len(most_liked) >= 10:  # 若頻道總影片數大於等於十，印出前十名影片
    for video in most_liked:
        temporary_list.append(video['snippet']['title'])  # 影片名稱
        temporary_list.append(video['statistics']['viewCount'])  # 該影片觀看數
        a = int(video['statistics']['likeCount'])
        b = int(video['statistics']['dislikeCount'])
        temporary_list.append(format(a / b, '0.2f'))  # 讚踩比
        temporary_list.append(video['statistics']['commentCount'])  # 評論數
        temporary_list.append(video['snippet']['publishedAt'])  # 影片上傳時間
        temporary_list.append("https://www.youtube.com/watch?v=" +
                              video['id'])  # 影片連結
        final_list.append(temporary_list)
        temporary_list = []
        count += 1
        if count == 10:
            break
    print(final_list)
else:
    print("Sorry, the total number videos of this channel is less than 10.")
