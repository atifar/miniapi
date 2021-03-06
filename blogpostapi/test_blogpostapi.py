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


def test_check_sanity(client):
    resp = client.get('/sanity')
    assert resp.status_code == 200
    assert 'Sanity still intact.' == resp.data.decode()


def test_get_all_blogposts(client):
    title = ['How to yodel', 'Why is the sky blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    for idx, t in enumerate(title):
        post = Post(title=t, body=body[idx])
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


def test_create_blogpost(client):
    title = ['How to yodel', 'Why the sky is blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    resp = client.post(
        '/post',
        json={
            'title': title[0],
            'body': body[0]
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    resp_data = resp.get_json()
    assert 'title' in resp_data
    assert 'body' in resp_data
    assert 'post_id' in resp_data
    assert resp_data['title'] == title[0]
    assert resp_data['body'] == body[0]
    assert resp_data['post_id'] == 1


def test_create_blogpost_missing_title(client):
    resp = client.post(
        '/post',
        json={
            'body': 'Just some body text.'
        },
        content_type='application/json'
    )
    assert resp.status_code == 400
    resp_data = resp.get_json()
    assert 'error' in resp_data
    assert resp_data['error'] == 'Please provide the title of the post!'


def test_create_blogpost_missing_body(client):
    resp = client.post(
        '/post',
        json={
            'title': 'A title'
        },
        content_type='application/json'
    )
    assert resp.status_code == 400
    resp_data = resp.get_json()
    assert 'error' in resp_data
    assert resp_data['error'] == 'Please provide the body of the post!'


def test_create_blogpost_incorrect_content_type(client):
    resp = client.post(
        '/post',
        json={
            'title': 'A title',
            'body': 'Just some body text.'
        },
        content_type='application/x-www-form-urlencoded'
    )
    assert resp.status_code == 400
    resp_data = resp.get_json()
    assert 'error' in resp_data
    assert resp_data['error'] == 'Please use application/json content type!'


def test_delete_blogpost(client):
    title = ['How to yodel', 'Why is the sky blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    for idx, t in enumerate(title):
        post = Post(title=t, body=body[idx])
        db.session.add(post)
    db.session.commit()
    resp = client.delete('/delete_post?id=1', content_type='application/json')
    assert resp.status_code == 204


def test_delete_blogpost_missing_id(client):
    title = ['How to yodel', 'Why is the sky blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    for idx, t in enumerate(title):
        post = Post(title=t, body=body[idx])
        db.session.add(post)
    db.session.commit()
    resp = client.delete('/delete_post', content_type='application/json')
    assert resp.status_code == 400
    resp_data = resp.get_json()
    assert 'error' in resp_data
    assert 'Please provide the pk of the post to delete' in resp_data['error']


def test_delete_non_existent_blogpost(client):
    title = ['How to yodel', 'Why is the sky blue']
    body = ['Practice a lot, grasshopper!', 'It only appears blue.']
    for idx, t in enumerate(title):
        post = Post(title=t, body=body[idx])
        db.session.add(post)
    db.session.commit()
    resp = client.delete('/delete_post?id=5', content_type='application/json')
    assert resp.status_code == 404
    resp_data = resp.get_json()
    assert 'error' in resp_data
    assert resp_data['error'] == 'There is no blog post with id: 5 in the DB.'
