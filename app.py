from flask import Flask, render_template, request
from dashboard import comments

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    data = []
    total_likes = 0
    total_comments = 0

    if request.method == "POST":

        url = request.form["url"]

        video_id = url.split("v=")[1].split("&")[0]

        data = comments(video_id)
        positive = sum(1 for c in data if c["sentiment"] == "Positive")

        negative = sum(
            1 for c in data
            if c["sentiment"] == "Negative"
        )

        neutral = sum(
            1 for c in data
            if c["sentiment"] == "Neutral"
        )
        total_comments = len(data)

        total_likes = sum(
            c.get("likes", 0)
            for c in data
        )
    return render_template(
    "comments.html",
    comments=data,
    total_comments=total_comments,
    total_likes=total_likes,
    positive=positive,
    negative=negative,
    neutral=neutral
     )
    
if __name__ == "__main__":
    app.run(debug=True)
