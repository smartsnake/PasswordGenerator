
from flask import Flask, request, jsonify
from bson.json_util import dumps
import json
import os
from util.MongoUtil import MongoUtil
from util.Generator import Generator

def create_application():
    application = Flask(__name__)

    # Helper classes
    mongoUtil = MongoUtil()
    gen = Generator()

    #Check if a string can be converted to int
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    # Create new database from new user
    @application.route("/NewUser", methods=['POST'])
    def new_user():
        try:
            if(request.is_json):
                account = request.get_json()
                mongoUtil.newDatabase(account['id'])
                return "OK", 200
            else:
                return 'Error in creating database.', 400
        except Exception as e:
            print({'error': str(e)})

    # Send (soon to be) encrypted data to user
    @application.route("/UserData", methods=['GET'])
    def user_data():
        try:
            if(request.is_json):
                account = request.get_json()
                return jsonify(dumps(mongoUtil.getCollection(account['id'])))
            else:
                return 'Error in getting database.', 401
        except Exception as e:
            print({'error': str(e)})

    # Add (soon to be) encrypted info to that users database
    @application.route("/NewPassword", methods=['PUT'])
    def new_password():
        try:
            if(request.is_json):
                json_object = request.get_json()
                account = json_object['account']
                record = json_object['record']

                assert account is not None

                # Must have these fields
                assert record["website"] is not None
                assert record["username"] is not None
                assert record["password"] is not None
                assert account['id'] is not None

                if mongoUtil.addRecordRemote(account['id'], record):
                    return "OK"
                else:
                    return "Error", 400
            else:
                return 'Error in saving new record.', 400
        except Exception as e:
            return {'error': str(e)}

    @application.route("/GeneratePassword", methods=['GET'])
    def generate_password():
        try:
            if(request.is_json):
                gen_prop = request.get_json()
                length = 15
                if gen_prop['length'] is not None:
                    length = int(gen_prop['length'])
                return dumps({'password': gen.generate_password(length)}), 200
            else:
                length = 15
                return dumps({'password': gen.generate_password(length)}), 200

        except Exception as e:
            return {'error': str(e)}

    return application

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application = create_application()
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
