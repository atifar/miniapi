import json
import os

from flask import Flask, jsonify, request, Response
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


def build_response(resp, status_code):
    """
    Helper function to build JSON responses (success and error).
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(resp),
        status=status_code
    )


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


@app.route('/post', methods=['POST'])
def post():
    req_data = request.get_json()
    if 'title' in req_data:
        title = str(req_data['title'])
    else:
        error_msg = {
            'error': 'Please provide the title of the post!'
        }
        return build_response(error_msg, 400)
    if 'body' in req_data:
        body = str(req_data['body'])
    else:
        error_msg = {
            'error': 'Please provide the body of the post!'
        }
        return build_response(error_msg, 400)
    post = Post(title=title, body=body)
    db.session.add(post)
    db.session.commit()
    last_post = Post.query.order_by(Post.post_id)[-1]
    msg = {'title': title, 'body': body, 'post_id': last_post.post_id}
    return build_response(msg, 201)
