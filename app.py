from googleapiclient.discovery import build

key="api key shouldnt be made public :-)"
youtube=build("youtube","v3",developerKey=key)

def comments(videoId):
    arr=[]
    a=youtube.commentThreads().list(
        part="snippet",
        videoId="LKNHVDPKy7g",
        maxResults=100
    )
    res=a.execute()
    for j in res["items"]:
        comment = j["snippet"]["topLevelComment"]["snippet"]
        arr.append({
            "author":comment["authorDisplayName"],
            "text":comment["textDisplay"],
            "likes":comment["likeCount"]
        })
    return arr


comment = comments("LKNHVDPKy7g")
for c in comment[:5]:
    print(c)
