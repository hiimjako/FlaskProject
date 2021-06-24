# FlaskProject

This is the internet, web and cloud exam project, developed in flask

# How to run this project

- Add ADMIN_EMAIL and ADMIN_PASSWORD to .env
- docker-compose -f docker-compose-dev.yml up 

- docker exec -it flask-app /bin/bash
  - flask db upgrade
  - flask setup_dev
- Open http://127.0.0.1:5000/
  - Log in with ADMIN_EMAIL and ADMIN_PASSWORD

Or it's aviable on [opendrive.site](https://opendrive.site/ "Site homepage")
# Flask migrate

Inizialize migration `flask db init`
Commit migration `flask db migrate -m ""`

Apply migrations `flask db upgrade`

If there are some trubles with "psycopg2" remove it from requirements.txt or use docker instead

**# TODO**

- add file size to db, for limit the amount of file to upload per user
- System manager
- Name to pdf while download in new page
- Invite user via email
- Change password, with rq queue to recrypt all files
- Add rq thats handles file inputs
- Add folders in drive
