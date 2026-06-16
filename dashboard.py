from googleapiclient.discovery import build
import mysql.connector
from sentiment import get_sentiment

key="AIzaSyDunGRWEClfAf4-H7mgSWs6gSzPjuNUal4"
youtube=build("youtube","v3",developerKey=key)

def comments(videoId):
    arr=[]
    a=youtube.commentThreads().list(
        part="snippet",
        videoId=videoId,
        maxResults=100
    )
    res=a.execute()
    for j in res["items"]:
        comment = j["snippet"]["topLevelComment"]["snippet"]
        arr.append({
        "author": comment["authorDisplayName"],
        "comment_text": comment["textDisplay"],
        "likes": comment["likeCount"],
        "sentiment": get_sentiment(
            comment["textDisplay"]
        )
    })
    print(arr[-1])
    return arr


comment = comments("LKNHVDPKy7g")
for c in comment[:5]:
    print(c)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwerty",
    database="youtube_dashboard"
)
cursor=conn.cursor()
for c in comment:

    query=""" INSERT INTO comments(author, comment_text, likes) VALUES (%s,%s,%s)"""
    values = (c["author"],c["comment_text"],c["likes"])
    cursor.execute(query, values)

conn.commit()

print("Connected!")