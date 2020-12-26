# import library
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import re

api_key = 'AIzaSyABgOEaH7Y49Ns-qPk5d8BBRwUeuZMs-Rw'
youtube = build('youtube', 'v3', developerKey=api_key)

pl_url = input()

pl_id = (pl_url[(pl_url.find("list=")+5):pl_url.find("&ab_channel=")])  # 抓取playlist id
print(pl_id)
order = input()  # 決定排序


def playlist_time(pl_id):
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')
    total_seconds = 0

    nextPageToken = None
    try:
        while True:
            pl_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=pl_id,
                maxResults=50,  # 一個清單裡有多個video，且總影片數目大過於五
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

        print("清單影片數量：" + str(len(vid_ids)) + " 影片總時長：" + f'{hours}:{minutes}:{seconds}')  # 62:9:43

    except:
        print("Sorry...Something went wrong")


playlist_time(pl_id)


# playlist 排序
def playlist_search(pl_id, order):
    videos = []

    nextPageToken = None

    try:
        while True:
            pl_request = youtube.playlistItems().list(
                part='contentDetails,snippet',
                playlistId=pl_id,
                maxResults=50,  # 一個清單裡有多個video，且總影片數目大過於五
                pageToken=nextPageToken
            )

            pl_response = pl_request.execute()
            #########
            vid_ids = []
            for item in pl_response['items']:
                vid_ids.append(item['contentDetails']['videoId'])

            vid_request = youtube.videos().list(
                part="statistics, snippet",
                id=','.join(vid_ids)
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                vid_views = item['statistics']['viewCount']
                if int(item['statistics']['likeCount']) == 0:
                    vid_like = 1
                else:
                    vid_like = int(item['statistics']['likeCount'])
                if int(item['statistics']['dislikeCount']) == 0:
                    vid_dislike = 1
                else:
                    vid_dislike = int(item['statistics']['dislikeCount'])
                like_dislike_ratio = '%.3f'%(int(vid_like) / int(vid_dislike))
                vid_favorite = item['statistics']['favoriteCount']
                vid_comment = item['statistics']['commentCount']
                vid_title = item['snippet']['title']
                date = item['snippet']['publishedAt']

                vid_id = item["id"]
                yt_link = f'http://youtu.be/{vid_id}'
                # date = item

                videos.append(
                    {
                        "title": vid_title,
                        "views": int(vid_views),
                        "like": int(vid_like),
                        "dislike": int(vid_dislike),
                        "like_dislike_ratio": like_dislike_ratio,
                        "favorite": vid_favorite,
                        "comment": int(vid_comment),
                        "date": date,
                        "url": yt_link

                    }
                )

            nextPageToken = pl_response.get('nextPageToken')

            if not nextPageToken:
                break

        videos.sort(key=lambda vid: vid[order], reverse=True)

        return_list = []
        for video in videos[:10]:  # 前十名關鎧次數清單
            return_list.append([video["title"], video["views"], video["like_dislike_ratio"],
                  video["comment"], video["date"], video["url"]])
        print(return_list)
        return return_list

    except:
        print("Sorry...Something went wrong")


playlist_search(pl_id, order)

