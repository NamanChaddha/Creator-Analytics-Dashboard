from googleapiclient.discovery import build
import mysql.connector

key="AIzaSyDunGRWEClfAf4-H7mgSWs6gSzPjuNUal4"
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
        print(comment)
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
    values = (c["author"],c["text"],c["likes"])
    cursor.execute(query, values)

conn.commit()

print("Connected!")