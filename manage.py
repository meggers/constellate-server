import os
import argparse

from server import app, db, session
from server.models import *

def create_db():
    db.create_all()

def drop_db():
    db.drop_all()

def seed_db():
    # add the users
    user_ids = []
    users = ["default","nick","matt","max"]
    for name in users:
        new_user = User(username=name, email="{}@email.com".format(name), password="default")
        session.add(new_user)
        session.commit()
        user_ids.append(new_user.id)

    return

def main():
    parser = argparse.ArgumentParser(description='Manage the Constellate db')
    parser.add_argument('command', help='the name of the command you want to run')
    parser.add_argument('--seedfile', help='the file with data for seeding the database')
    args = parser.parse_args()

    if args.command == 'create_db':
        create_db()
        print "db created!"

    elif args.command == 'delete_db':
        drop_db()
        print "db deleted!"

    elif args.command == 'seed_db':
        seed_db()
        print "db deleted!"

if __name__ == '__main__':
    main()
