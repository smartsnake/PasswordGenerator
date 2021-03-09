import sys
import argparse
from util.MongoUtil import MongoUtil
from util.Generator import Generator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates new passwords and adds them to mondodb.')

    parser.add_argument('--length', '-l', action='store', default='15', dest='length',
                        help='Password length to be generated. (default=15)')

    parser.add_argument('-s', '--search', nargs=2, action='store', dest='search',
                        help='Used to search for existing password records.\n'
                        +'Usage: python main.py --search website example.com')

    args = parser.parse_args()

    mongoUtil = MongoUtil()
    gen = Generator()

    try:
        search = args.search
        pass_len = int(args.length)

        if search is None or len(search) != 2:
            website = input("Enter website: ")
            username = input("Enter username/email: ")
            password = gen.generate_password(pass_len)
            print(f"Password: {password}, Len: {len(password)}")

            record = {"website":website, "username":username, "password":password}

            if mongoUtil.addRecord(record):
                print("Record added.")
            else:
                print("Recorded failed.")

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