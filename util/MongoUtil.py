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
            # print('Connected to mongodb')
        except Exception as e:
            print('Failed to connect to mongodb')
    
    # Creates new database for new users
    # TODO: Encrype database using users unique key.
    def newDatabase(self, user_id):
        try:
            new_database = self.client[user_id]
            password_coll = new_database['PasswordCollection']

            # You have to insert a record in order to create database/collections.
            password_coll.insert_one({'website:': 'DELETE', 'username': 'DELETE', 'password': 'DELETE'})
            # Delete unused record
            password_coll.delete_one({'website:': 'DELETE', 'username': 'DELETE', 'password': 'DELETE'})
            return True
        except Exception as e:
            return False, {'Error': e}

    # Returns all passwords
    def getCollection(self, user_id):
        try:
            return self.client[user_id]['PasswordCollection'].find({}, {'_id':0, 'website':1, 'username':1, 'password':1})
        except Exception as e:
            return {'Error' : e}

    #Record is tuple with 2 fields, record[0] is website, record[1] is username/email, and record[2] is salted password
    def addRecordRemote(self, user_id, record):
        try:
            assert len(record) == 3
            #Check if user_id database exists
            #assert user_id in self.client.list_database_names()

            self.client[user_id]['PasswordCollection'].insert_one(record)
            return True
        except Exception as e:
            return False, e

    #Record is tuple with 2 fields, record[0] is website, record[1] is username/email, and record[2] is salted password
    def addRecord(self, record):
        try:
            assert len(record) == 3
            self.coll.insert_one(record)
            return True
        except Exception as e:
            return False

    #Import csv lastpass into database
    def importLastPass(self, fileLocation):
        try:
            df = pd.read_csv(fileLocation)
            df = df[['name', 'username', 'password']]
            df.columns = ['website', 'username', 'password']
            records = json.loads(df.T.to_json()).values()
            self.coll.insert_many(records)
        except Exception as e:
            print('Import Failed.')


    #Searchs if a website already has a password, searchField is [username/email, website]
    def searchRecord(self, user_id, searchField, searchText):
        assert searchField in self.searchableFields
        return self.client[user_id]['PasswordCollection'].find_one(({searchField: searchText}), {'_id':0, 'website':1, 'username':1, 'password':1})
        

    #Searchs if a website already has a password, searchField is [username/email, website]
    def searchRecord(self, searchField, searchText):
        assert searchField in self.searchableFields
        return self.coll.find_one(({searchField: searchText}), {'_id':0, 'website':1, 'username':1, 'password':1})

    def printCollection(self):
        for row in self.coll:
            print(row)