import requests
yt = 'AIzaSyDiGgYRJ0Z5AvTSinAII1XwFGlBEWRYTKQ'
params = {
    'part':'snippet',
    'q':'muhfaad',
    'regionCode': 'in',
    'type':'video',
    'maxResults':'5',
    'key': yt
    
}

data = requests.get('https://www.googleapis.com/youtube/v3/search',params=params)
id = data.json()['items'][0]['id']['videoId']
title = data.json()['items'][0]['snippet']['title']
channel_name = data.json()['items'][0]['snippet']['channelTitle']
print(id,title,channel_name)

# GET https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q=muhfaad&regionCode=in&type=video&key=[YOUR_API_KEY] HTTP/1.1

# Authorization: Bearer [YOUR_ACCESS_TOKEN]
# Accept: application/json
