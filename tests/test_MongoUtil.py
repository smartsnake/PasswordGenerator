import pytest
import json
from util.MongoUtil import MongoUtil

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

@pytest.fixture
def test_Constructor():
    return MongoUtil()

#Tests creating a new database
def test_newDatabase(test_Constructor):
    user_id = '0001'
    client = test_Constructor

    assert client.newDatabase(user_id)

def test_addRecordRemote(test_Constructor):
    user_id = '0001'
    record = {'website': 'example.com', 'username': 'username', 'password':'password'}
    client = test_Constructor

    assert client.addRecordRemote(user_id, record)

def test_getCollection(test_Constructor):
    user_id = '0001'
    client = test_Constructor

    responce = client.getCollection(user_id)

    assert responce is not None