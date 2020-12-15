def Playlists_Count(channelid):
    content = youtube_api.playlists().list(channelId=channelid,
                                           part='snippet').execute()
    playlist_count = content['pageInfo']['totalResults']
    return playlist_count
