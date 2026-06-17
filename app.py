from flask import Flask, render_template, request, send_file
from dashboard import comments

from collections import Counter
import re

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

app = Flask(__name__)

# Global variables for PDF
total_comments = 0
total_likes = 0
positive = 0
negative = 0
neutral = 0
question_count = 0
questions_list = []
common_words = []
top_comments = []


@app.route("/", methods=["GET", "POST"])
def home():

    global total_comments
    global total_likes
    global positive
    global negative
    global neutral
    global question_count
    global common_words
    global top_comments
    global questions_list

    data = []

    total_comments = 0
    total_likes = 0
    positive = 0
    negative = 0
    neutral = 0
    question_count = 0
    
    if request.method == "POST":

        url = request.form["url"]

        video_id = url.split("v=")[1].split("&")[0]

        data = comments(video_id)

        # Top comments
        top_comments = sorted(
            data,
            key=lambda x: x["likes"],
            reverse=True
        )[:5]

        # Sentiment counts
        positive = sum(
            1 for c in data
            if c["sentiment"] == "Positive"
        )

        negative = sum(
            1 for c in data
            if c["sentiment"] == "Negative"
        )

        neutral = sum(
            1 for c in data
            if c["sentiment"] == "Neutral"
        )

        # Questions
        question_count = sum(
            1 for c in data
            if c.get("is_question", False)
        )
        questions_list = [
        c["comment_text"]
        for c in data
        if c.get("is_question", False)
    ]
        total_comments = len(data)

        total_likes = sum(
            c.get("likes", 0)
            for c in data
        )

        # Trending Keywords
        words = []

        stop_words = {
            "the","and","you","for","this",
            "that","with","are","was","have",
            "your","from","they","not","but",
            "all","can","will","just","how",
            "what","when","where","who","why"
        }

        for c in data:

            text = c["comment_text"].lower()

            found_words = re.findall(
                r'\b[a-z]{3,}\b',
                text
            )

            for word in found_words:

                if word not in stop_words:
                    words.append(word)

        common_words = Counter(words).most_common(10)

    return render_template(
        "comments.html",
        comments=data,
        total_comments=total_comments,
        total_likes=total_likes,
        positive=positive,
        negative=negative,
        neutral=neutral,
        question_count=question_count,
        common_words=common_words,
        top_comments=top_comments
    )


@app.route("/download_report")
def download_report():

    pdf_file = "report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    # Title
    title_style = styles["Title"]
    title_style.textColor = colors.red

    content.append(
        Paragraph(
            "YouTube Creator Analytics Report",
            title_style
        )
    )

    content.append(Spacer(1, 20))

    # Stats Table
    stats = [
        ["Comments", "Likes", "Questions"],
        [
            str(total_comments),
            str(total_likes),
            str(question_count)
        ]
    ]

    stats_table = Table(stats, colWidths=150)

    stats_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.red),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,1),(-1,1),colors.whitesmoke),

        ('GRID',(0,0),(-1,-1),2,colors.black),

        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    content.append(stats_table)

    content.append(Spacer(1,20))

    # Sentiment Table
    sentiment = [
        ["Sentiment","Count"],
        ["Positive", positive],
        ["Negative", negative],
        ["Neutral", neutral]
    ]

    sentiment_table = Table(sentiment)

    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,1),(-1,1),colors.lightgreen),
        ('BACKGROUND',(0,2),(-1,2),colors.pink),
        ('BACKGROUND',(0,3),(-1,3),colors.lightgrey),

        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))

    content.append(sentiment_table)

    content.append(Spacer(1,20))

    # Keywords
    content.append(
        Paragraph(
            "Trending Keywords",
            styles["Heading2"]
        )
    )

    for word, count in common_words:

        content.append(
            Paragraph(
                f"{word} ({count})",
                styles["Normal"]
            )
        )

    content.append(Spacer(1,20))
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Questions Asked: {question_count}",
            styles["Heading2"]
        )
    )
    for q in questions_list:

        content.append(
            Paragraph(
                "• " + q,
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1,5)
        )

    doc.build(content)

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)