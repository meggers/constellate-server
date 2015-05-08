import os
import csv
import argparse

from server import app, db, session, settings
from server.models import *

def create_db():
    db.create_all()

def drop_db():
    db.drop_all()

def seed_db():
    # add default user
    default_user = User(username="default", email="default@email.com", password="default")
    session.add(default_user)
    session.commit()

    # add all stars
    with open(settings.STAR_FILE, 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            id = int(row[settings.ID_INDEX])
            ra = float(row[settings.RA_INDEX])
            dec = float(row[settings.DEC_INDEX])
            mag = float(row[settings.MAG_INDEX])

            star = Star(id=id, ra=ra, dec=dec, mag=mag)
            session.add(star)

    session.commit()

    # add all constellations
    with open(settings.CONST_FILE, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[settings.NAME_INDEX]
            a, b = int(row[settings.A_INDEX]), int(row[settings.B_INDEX])

            constellation = session.query(Constellation).filter_by(name=name).first()
            if not constellation:
                constellation = Constellation(user_id=default_user.id, name=name)
                session.add(constellation)
                session.commit()

            vector = Vector(constellation_id=constellation.id, a=a, b=b)
            session.add(vector)
            session.commit()


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
        print "db seeded!"

if __name__ == '__main__':
    main()
