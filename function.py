# import library
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

api_key = 'AIzaSyABgOEaH7Y49Ns-qPk5d8BBRwUeuZMs-Rw'
youtube_api = build('youtube', 'v3', developerKey = api_key)

# searching keywords
search_items = str(input()) 

def Youtube_search(query, max_results=50, order="relevance", token=None, location=None, location_radius=None):

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
            viewCount.append(stats['items'][0]['statistics']['viewCount'])

            # not every video has likes/dislikes enabled so they won't appear in JSON response
            try:
                likeCount.append(stats['items'][0]['statistics']['likeCount'])
            except:
                # good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                             stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                # appends "Not Available" to keep dictionary values aligned
                likeCount.append("Not available")
                
            try:
                dislikeCount.append(stats['items'][0]['statistics']['dislikeCount'])     
            except:
                # good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Dislikes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                                stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                dislikeCount.append("Not available")

            # sometimes comments are disabled so if they exist append, if not append nothing...
            # it's not uncommon to disable comments, so no need to wrap in try and except  
            if 'commentCount' in stats['items'][0]['statistics'].keys():
                commentCount.append(stats['items'][0]['statistics']['commentCount'])
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
