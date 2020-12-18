# import library
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import re

api_key = 'AIzaSyABgOEaH7Y49Ns-qPk5d8BBRwUeuZMs-Rw'
youtube_api = build('youtube', 'v3', developerKey=api_key)

# searching keywords
search_items = str(input())

# excluding keywords
exclude_items = ' -' + str(input())

# query
query = search_items + exclude_items

# specifies the method that will be used to order resources
choose_order = str(input())
# 'date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'

def video_search(query, max_results=50, order=choose_order, token=None, location=None, location_radius=None):

    # search upto max 50 videos based on query
    search_response = youtube_api.search().list(q=query,
                                                type="video",
                                                pageToken=token,
                                                order=order,
                                                part="id, snippet",
                                                maxResults=max_results,
                                                location=location,
                                                locationRadius=location_radius).execute()
    items = search_response['items']

    if len(items) == 0:
        print('Find Nothing')
    else:
        # assign values
        title = items[0]['snippet']['title']
        channelId = items[0]['snippet']['channelId']
        datePublished = items[0]['snippet']['publishedAt']

    return search_response
    
def store_results(response):
    
    # create variables to store your values
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    like_dislike_ratio = []
    commentCount = []
    category = []
    tags = []
    videos = []
    datePublished = []
    url = []
    
    for search_result in response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            # append title, video and published date for each item
            title.append(search_result['snippet']['title'])
            videoId.append(search_result['id']['videoId'])
            url.append('https://www.youtube.com/watch?v=' + search_result['id']['videoId'])
            datePublished.append(search_result['snippet']['publishedAt'])

            # then collect stats on each video using videoId
            stats = youtube_api.videos().list(part='statistics, snippet',
                                          id=search_result['id']['videoId']).execute()
            
            channelId.append(stats['items'][0]['snippet']['channelId']) 
            channelTitle.append(stats['items'][0]['snippet']['channelTitle']) 
            categoryId.append(stats['items'][0]['snippet']['categoryId']) 
            viewCount.append(int(stats['items'][0]['statistics']['viewCount']))

            # not every video has likes/dislikes enabled so they won't appear in JSON response
            try:
                likeCount.append(int(stats['items'][0]['statistics']['likeCount']))
            except:
                # good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                             stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                # appends "Not Available" to keep dictionary values aligned
                likeCount.append("Not available")
                
            try:
                dislikeCount.append(int(stats['items'][0]['statistics']['dislikeCount']))     
            except:
                # good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Dislikes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                                stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                dislikeCount.append("Not available")

            try:
                like = int(stats['items'][0]['statistics']['likeCount'])
                dislike = int(stats['items'][0]['statistics']['dislikeCount'])
                # if dislike is zero, append its value
                if dislike == 0:
                    dislike = 0.5
                like_dislike_ratio.append(like / dislike)
            except:
                like_dislike_ratio.append("Not available")

            # sometimes comments are disabled so if they exist append, if not append nothing...
            # it's not uncommon to disable comments, so no need to wrap in try and except  
            if 'commentCount' in stats['items'][0]['statistics'].keys():
                commentCount.append(int(stats['items'][0]['statistics']['commentCount']))
            else:
                commentCount.append(0)
         
            if 'tags' in stats['items'][0]['snippet'].keys():
                tags.append(stats['items'][0]['snippet']['tags'])
            else:
                # I'm not a fan of empty fields
                tags.append("No Tags")
                
    # break out of for-loop and if statement and store lists of values in list
    youtube_list = [tags, channelId, channelTitle, categoryId, title, videoId,
                    viewCount, likeCount, dislikeCount, like_dislike_ratio, 
                    commentCount, datePublished, url]
 
    return youtube_list

# function 讚踩比
def like_dislike(result):
    portfolio = []
    for i in range(50):
        portfolio += [[result[4][i], result[6][i], result[9][i], result[10][i], result[11][i], result[12][i]]]
    portfolio.sort(key=lambda x:x[2], reverse=True)

    # just list the top 10
    return portfolio[0:10]

# function 影片觀看數
def viewcount(result):
    portfolio = []
    for i in range(50):
        portfolio += [[result[4][i], result[6][i], result[9][i], result[10][i], result[11][i], result[12][i]]]
    portfolio.sort(key=lambda x:x[1], reverse=True)

    # just list the top 10
    return portfolio[0:10] 

# function 留言數
def commentcount(result):
    portfolio = []
    for i in range(50):
        portfolio += [[result[4][i], result[6][i], result[9][i], result[10][i], result[11][i], result[12][i]]]
    portfolio.sort(key=lambda x:x[3], reverse=True)

    # just list the top 10
    return portfolio[0:10]
    
like_dislike(store_results(video_search(query)))
viewcount(store_results(video_search(query)))
commentcount(store_results(video_search(query)))


def dataframe(result):
    df = pd.DataFrame(result).transpose()
    df.columns = ['tags', 'channelId', 'channelTitle', 'categoryId', 'title', 'videoId',
                  'viewCount', 'likeCount', 'dislikeCount', 'like_dislike_ratio', 'commentCount']
    
    return df

result_df = dataframe(store_results(video_search(query)))

# 使用者決定想要篩選的ｙ值以及x 值，並輸出圖表（例如他想要比較各個頻道x的關鍵字為python的影片瀏覽數y）
def sort_data(select1,select2):
    select_data = result_df.sort_values(by=str(select1), ascending=False).head(10)   # 選出前十名
    plt.bar(select_data[select2], select_data[select1])
    plt.xticks(rotation=90)   # x值轉換成垂直
    plt.show()

# 範例試跑程式
sort_data('viewCount','channelId')


# 計算清單時長
def playlist_time(pl_id):
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')
    total_seconds = 0

    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=pl_id,
            maxResults=50,          # 一個清單裡有多個video，且總影片數目大過於五
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += video_seconds

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    print(f'{hours}:{minutes}:{seconds}')  # 62:9:43




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

# 範例試跑程式
videos = get_channel_videos('UCkUq-s6z57uJFUFBvZIVTyg')
res = youtube.videos().list(id=videos[0]['snippet']['resourceId']['videoId'], part='statistics').execute()


def get_video_stats(video_ids):#找出頻道所有影片的數據
    stats = []
    for i in range(0, len(video_ids), 50):
        res=youtube.videos().list(id=','.join(video_ids[i:i+50]), part='statistics').execute()
        stats += res['items']
    return stats


# 範例試跑程式
video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))
stats = get_video_stats(video_ids)
count = 0
most_liked = sorted(stats, key=lambda x:int(x['statistics']['likeCount']), reverse=True)
for video in most_liked:#列出讚數最多的前十支影片
    print(""https://www.youtube.com/watch?v="+video['id'], video['statistics']['likeCount'])
    count += 1
    if count == 10:
        break
