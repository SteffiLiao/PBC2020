import urllib.request

import json

print("Please enter your youtube channel ID")
name = input()  #輸入頻道的id

key = 'AIzaSyDCnkRjeXJLQmXK30A4YXnOWsi-7RwxTb4'


data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+name+"&key="+key).read() #讀取資料
total_view=json.loads(data)['items'][0]['statistics']['viewCount']
print("You have %d" % int(total_view) + "total view")