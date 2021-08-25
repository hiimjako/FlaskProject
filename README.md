# FlaskProject

This is the internet, web and cloud exam project, developed in flask

# How to run this project

- Copy .env.sample into .env
- Fill the missing fields (like: passwords)
  - MAIL_USERNAME and MAIL_PASSWORD are the credential to send the invitation link to join the application, it should be a gmail account, leave empty and it will use the default ones
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
- Name to pdf while download in new page
- Backup button
- Change password, with rq queue to recrypt all files
- Add rq thats handles file inputs
