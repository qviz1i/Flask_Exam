from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    intro = db.Column(db.String(300))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())








@app.route("/")
def home():
    return render_template("index.html")


@app.route("/articles")
def articles():
    articles = Article.query.all()
    return render_template("articles.html", articles=articles)


@app.route("/create-article", methods=["GET", "POST"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        with app.app_context():
            db.create_all()

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")

        except Exception as e:
            print(e)
            return "Ошибка"


    else:
        return render_template("create_article.html")




if __name__ == "__main__":
    app.run(debug=True)

