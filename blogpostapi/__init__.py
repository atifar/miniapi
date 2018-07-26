import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

blogpostapi_dir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(blogpostapi_dir, 'blog.db')

app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=db_path,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    body = db.Column('body', db.String)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return f'Post "{self.title}" (id: {self.post_id})'


@app.route('/sanity')
def sanity():
    return 'Sanity still intact.'


@app.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    obj_array = []
    for post in posts:
        obj = {
            'post_id': post.post_id,
            'title': post.title,
            'body': post.body
        }
        obj_array.append(obj)
    resp = jsonify(obj_array)
    resp.status_code = 200
    return resp
