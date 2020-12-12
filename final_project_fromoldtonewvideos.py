from datetime import datetime
from googleapiclient.discovery import build
api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
youtube = build('youtube', 'v3', developerKey=api_key)
type(youtube)
start_time = datetime(year=2005, month=1, day=1).strftime(
    '%Y-%m-%dT%H:%M:%SZ')  # 想要搜尋的範圍
end_time = datetime(year=2008, month=1, day=1).strftime(
    '%Y-%m-%dT%H:%M:%SZ')  # 想要搜尋的範圍
req = youtube.search().list(
    q='python programming',  # 要搜的關鍵字
    part='snippet',
    type='video',  # 可以找影片也可以找頻道
    maxResults=50,
    publishedAfter=start_time,
    publishedBefore=end_time)  # maxresults會影響第十行items的數量
res = req.execute()
for item in sorted(
        res['items'],
        key=lambda x: x['snippet']['publishedAt']):  # 按照時間從舊到新排序
    print(item['snippet']['title'], item['snippet']['publishedAt'],item['id']['videoId'])
    # print(item['snippet'])
