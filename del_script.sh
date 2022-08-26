rm db.sqlite3
rm -r photosite/migrations/
python3.10 manage.py makemigrations photosite
python3.10 manage.py migrate
