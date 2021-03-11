import pytest
from util.MongoUtil import MongoUtil

client = None

def test_Constructor():
    client = MongoUtil()
    assert client is not None

