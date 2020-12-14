# import library
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

api_key = 'AIzaSyABgOEaH7Y49Ns-qPk5d8BBRwUeuZMs-Rw'
youtube_api = build('youtube', 'v3', developerKey=api_key)

# searching keywords
search_items = str(input())

# specifies the method that will be used to order resources
choose_order = str(input())
# 'date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'

def Youtube_search(query, max_results=50, order=choose_order, token=None, location=None, location_radius=None):

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
    
    for search_result in response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            # append title and video for each item
            title.append(search_result['snippet']['title'])
            videoId.append(search_result['id']['videoId'])

            # then collect stats on each video using videoId
            stats = youtube_api.videos().list(part='statistics, snippet',
                                          id=search_result['id']['videoId']).execute()
            
            channelId.append(stats['items'][0]['snippet']['channelId']) 
            channelTitle.append(stats['items'][0]['snippet']['channelTitle']) 
            categoryId.append(stats['items'][0]['snippet']['categoryId']) 
            viewCount.append(int(stats['items'][0]['statistics']['viewCount']))   # int()為了之後輸出圖表

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
            
            like = int(stats['items'][0]['statistics']['likeCount'])
            dislike = int(stats['items'][0]['statistics']['dislikeCount'])
            # if dislike is zero, append its value
            if dislike == 0:
                dislike = 0.5
                like_dislike_ratio.append(like / dislike)
            like_dislike_ratio.append(like / dislike)
                
    # break out of for-loop and if statement and store lists of values in list
    youtube_list = [tags, channelId, channelTitle, categoryId, title, videoId,
                    viewCount, likeCount, dislikeCount, like_dislike_ratio, commentCount]
 
    return youtube_list
    
response = Youtube_search(search_items)
results = store_results(response)

# create dataframe
result_df = pd.DataFrame(results).transpose()
result_df.columns = ['tags', 'channelId', 'channelTitle', 'categoryId', 'title', 'videoId',
                     'viewCount', 'likeCount', 'dislikeCount', 'like_dislike_ratio', 'commentCount']

# sort it by like_dislike_ratio value
result_df.sort_values(by=['like_dislike_ratio'], ascending=False)

# 使用者決定想要篩選的ｙ值以及x 值，並輸出圖表（例如他想要比較各個頻道x的關鍵字為python的影片瀏覽數y）
def sort_data(select1,select2):
    select_data = result_df.sort_values(by=str(select1), ascending=False).head(10)   # 選出前十名
    plt.bar(select_data[select2], select_data[select1])
    plt.xticks(rotation=90)   # x值轉換成垂直
    plt.show()

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

