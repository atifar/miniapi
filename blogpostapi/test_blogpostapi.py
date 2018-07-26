import os
import tempfile

import pytest

from . import app, db, Post


@pytest.fixture
def client():
    db_fd, test_db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{test_db_path}'
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)


def test_get_all_blogposts(client):
    title = ['How to yodel', 'Why is the sky blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    post = Post(title=title[0], body=body[0])
    db.session.add(post)
    post = Post(title=title[1], body=body[1])
    db.session.add(post)
    db.session.commit()
    resp = client.get('/posts', content_type='application/json')
    assert resp.status_code == 200
    resp_data = resp.get_json()
    assert 2 == len(resp_data)
    for i in range(2):
        assert 'title' in resp_data[i]
        assert 'body' in resp_data[i]
        assert 'post_id' in resp_data[i]
        assert resp_data[i]['title'] == title[i]
        assert resp_data[i]['body'] == body[i]
        assert resp_data[i]['post_id'] == i + 1
