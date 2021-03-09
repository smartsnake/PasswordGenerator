import sys
from util.MongoUtil import MongoUtil
from util.Generator import Generator


if __name__ == '__main__':
    mongoUtil = MongoUtil()
    gen = Generator()

    if len(sys.argv) < 2:
        print("Pass password length as arg")
        sys.exit(0)

    try:
        arg1 = int(sys.argv[1])
        pass_len = int(arg1)

        website = input("Enter website: ")
        username = input("Enter username/email: ")

        password = gen.generate_password(pass_len)
        print(f"Password: {password}, Len: {len(password)}")

        record = {"website":website, "username":username, "password":password}

        if mongoUtil.addRecord(record):
            print("Record added.")
        else:
            print("Recorded failed.")


    except:
        print("Pass positive integer as arg")
        raise SystemExit(1)