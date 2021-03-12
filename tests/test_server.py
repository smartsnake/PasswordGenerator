from flask.helpers import url_for
from server import create_application
import pytest, json
from flask import Response, Flask

@pytest.fixture
def app():
    app = create_application()
    return app


headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

# Tests creating new user
def test_new_user(app):
    with app.test_client() as client:
        res = client.post("/NewUser", data=json.dumps({'id':'0002'}), headers=headers)
        assert res.status_code == 200

# Tests incorrect datatype
def test_new_user_fail(app):
    with app.test_client() as client:
        res = client.post("/NewUser", data='fialed')
        assert res.status_code != 200

# Tests getting user data
def test_user_data(app):
    with app.test_client() as client:
        res = client.get("/UserData", data=json.dumps({'id':'0002'}), headers=headers)
        assert res.status_code == 200
        assert res.content_type == 'application/json'

# Test bad getting user data
def test_user_data_failed(app):
    with app.test_client() as client:
        res = client.get("/UserData", data=json.dumps({'account':'0002'}), headers=headers)
        assert res.status_code != 200

# Test inserting new recored into user database
def test_new_password(app):
    with app.test_client() as client:
        res = client.put("/NewPassword", data=json.dumps({'account': {'id': '0002'}, 'record': {'website':'example.com', 'username': 'username', 'password': 'lamepassword'}}), headers=headers)
        assert res.status_code == 200

# Test bad inserting new recored into user database
def test_new_password(app):
    with app.test_client() as client:
        res = client.put("/NewPassword", data=json.dumps({'record': {'website':'example.com', 'username': 'username', 'password': 'lamepassword'}}))
        assert res.status_code != 200