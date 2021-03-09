import sys
import argparse
from util.MongoUtil import MongoUtil
from util.Generator import Generator

#Custom help messages
def help_msg(name=None):
    return '''main.py [-h] [--length LENGTH] [--search SEARCHFIELD SEARCHTEXT]
            '''
def search_usage():
    return'''python main.py --search website example.com
             python main.py --search username admin
    '''

if __name__ == '__main__':
    #Argument requirments
    parser = argparse.ArgumentParser(description='Creates new passwords and adds them to mondodb.', usage=help_msg())
    parser.add_argument('--length', '-l', action='store', default='15', dest='length',
                        help='Password length to be generated. (default=15)')

    parser.add_argument('--search','-s',  nargs=2, action='store', dest='search',
                        help='Used to search for existing password records.')
    args = parser.parse_args()


    mongoUtil = MongoUtil()
    gen = Generator()

    try:
        search = args.search
        pass_len = int(args.length)

        # Checks if search argument was previded
        if search is None or len(search) != 2:
            website = input("Enter website: ")
            username = input("Enter username/email: ")
            password = gen.generate_password(pass_len)

            record = {"website":website, "username":username, "password":password}

            #Save into database
            if mongoUtil.addRecord(record):
                print("Record added.")
            else:
                print("Recorded failed.")

        # Dont create password, search database instead.
        else:
            if search[0] not in mongoUtil.searchableFields:
                print(f'Searchable fields are [username or website]')
                raise SystemExit(1)
            else:
                record = mongoUtil.searchRecord(search[0], search[1])
                print(record)

    except:
        print("Pass positive integer as arg")
        raise SystemExit(1)