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
        if result[9][i] != 'Not available':
            portfolio += [[result[4][i], result[6][i], result[9][i], result[10][i], result[11][i], result[12][i]]]
    portfolio.sort(key=lambda x:x[2], reverse=True)

    # just list the top 10
    return portfolio[0:10]

# function 影片觀看數
def viewcount(result):
    portfolio = []
    for i in range(50):
        if result[6][i] != 'Not available':
            portfolio += [[result[4][i], result[6][i], result[9][i], result[10][i], result[11][i], result[12][i]]]
    portfolio.sort(key=lambda x:x[1], reverse=True)

    # just list the top 10
    return portfolio[0:10] 

# function 留言數
def commentcount(result):
    portfolio = []
    for i in range(50):
        if result[10][i] != 'Not available':
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
                  'viewCount', 'likeCount', 'dislikeCount', 'like_dislike_ratio', 'commentCount',
                  'datePublished', 'url']
    
    return df

result_df = dataframe(store_results(video_search(query)))


# 'tags', 'channelId', 'channelTitle', 'categoryId', 'title', 'videoId',
# 'viewCount', 'likeCount', 'dislikeCount', 'like_dislike_ratio', 'commentCount'

# 使用者決定想要篩選的ｙ值以及x 值，並輸出圖表（例如他想要比較各個頻道x的關鍵字為python的影片瀏覽數y）
def sort_data(select1, select2):
    select_data = result_df.sort_values(by=str(select1), ascending=False).head(10)   # 選出前十名
    plt.bar(select_data[select2], select_data[select1])
    plt.xticks(rotation=90)   # x值轉換成垂直
    plt.show()

# 範例試跑程式
sort_data('viewCount','channelId')



