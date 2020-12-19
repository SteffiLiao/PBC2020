from datetime import datetime
from googleapiclient.discovery import build
api_key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'
youtube = build('youtube', 'v3', developerKey=api_key)
res = youtube.channels().list(
    id='UCkUq-s6z57uJFUFBvZIVTyg',
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


videos = get_channel_videos('UCkUq-s6z57uJFUFBvZIVTyg')
res=youtube.videos().list(id=videos[0]['snippet']['resourceId']['videoId'],part='statistics').execute()
def get_video_stats(video_ids):
    stats=[]
    for i in range(0,len(video_ids),50):
        res=youtube.videos().list(id=','.join(video_ids[i:i+50]),part='statistics').execute()
        stats+=res['items']
    return stats
video_ids=list(map(lambda x:x['snippet']['resourceId']['videoId'],videos))
stats=get_video_stats(video_ids)
print(len(stats))
count=0
most_liked = sorted(stats, key=lambda x:int(x['statistics']['likeCount']), reverse=True)
for video in most_liked:
    print("https://www.youtube.com/watch?v="+video['id'], video['statistics']['likeCount'])
    count+=1
    if count==10:
        break