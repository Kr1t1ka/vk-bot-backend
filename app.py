from flask import Flask, render_template, request, redirect
from flask_restx import fields, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id


api = Api(app)
post_model = api.model('Post', model={'id': fields.Integer(description='The id', readonly=True),
                                      'Title': fields.String(description='The title', readonly=False),
                                      'Intro': fields.String(description='The intro', readonly=False),
                                      'Text': fields.String(description='The text', readonly=False),
                                      'Data': fields.DateTime(dt_format='rfc822')})

post_parser = api.parser()
post_parser.add_argument("post_id", required=False, location="args")
post_parser.add_argument("title", required=False, location="args")


def split_args(args: str) -> list:
    if "," in args:
        return args.split(",")
    return [args]


def split_dict_args(dict_args: dict) -> dict:
    return {
        key: split_args(value)
        for key, value in dict_args.items()
    }


@api.route('/api-post/<int:post_id>')
class Post(Resource):

    @api.expect(post_model)
    def put(self, id):
        post = api.payload

        article = Article.query.get(id)
        article.title = post['title']
        article.intro = post['intro']
        article.text = post['text']
        try:
            db.session.commit()
            return "Done"
        except:
            return "Error DB"

    @staticmethod
    def delete(post_id):
        article = Article.query.get_or_404(post_id)

        try:
            db.session.delete(article)
            db.session.commit()
        except:
            return "Error_DB"


@api.route('/api-post')
class AllPosts(Resource):
    @api.marshal_with(post_model)
    @api.expect(post_parser)
    def get(self):
        args = split_dict_args(request.args)

        if "post_id" in args:
            article = Article.query.filter(Article.id.in_(args["post_id"]))
        if "title" in args:
            article = Article.query.filter(Article.title.in_(args["title"]))

        articles = article.all()

        return articles

    @api.expect(post_model)
    def post(self):
        post = api.payload
        title = post['Title']
        intro = post['Intro']
        text = post['Text']

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
        except:
            return "Error_DB"


@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run(debug=False)
