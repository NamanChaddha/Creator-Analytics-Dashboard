from flask import Flask, render_template
from dashboard import comments

app = Flask(__name__)

@app.route("/")
def home():
    comment= comments("dQw4w9WgXcQ")

    return render_template("comments.html",comments=comment
    )

if __name__ == "__main__":
    app.run(debug=True)