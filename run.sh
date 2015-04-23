source flask/bin/activate
python manage.py delete_db
python manage.py create_db
python manage.py seed_db
./constellate-server.py
