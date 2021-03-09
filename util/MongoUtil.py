from pymongo import MongoClient
import pandas as pd
import json

class MongoUtil:
    def __init__(self, host='localhost', port=27017):
        #The only fields that are searchabel
        self.searchableFields = ['website','username']
        try:
            self.client = MongoClient(host, port)
            self.db = self.client["PasswordDatabase"]
            self.coll = self.db["PasswordCollection"]
            print('Connected to mongodb')
        except:
            print('Failed to connect to mongodb')

    #Record is tuple with 2 fields, record[0] is website, record[1] is username/email, and record[2] is salted password
    def addRecord(self, record):
        try:
            assert len(record) == 3
            self.coll.insert_one(record)
            return True
        except:
            return False

    #Import csv lastpass into database
    def importLastPass(self, fileLocation):
        try:
            df = pd.read_csv(fileLocation)
            df = df[['name', 'username', 'password']]
            df.columns = ['website', 'username', 'password']
            records = json.loads(df.T.to_json()).values()
            self.coll.insert_many(records)
        except:
            print('Import Failed.')


    #Searchs if a website already has a password, searchField is [username/email, website]
    def searchRecord(self, searchField, searchText):
        assert searchField in self.searchableFields
        return self.coll.find_one(({searchField: searchText}), {'_id':0, 'website':1, 'username':1, 'password':1})

    def printCollection(self):
        for row in self.coll:
            print(row)