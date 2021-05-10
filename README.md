**# FlaskProject**

This is the internet, web and cloud exam project, developed in flask


**# How to run this project**

- Add ADMIN_EMAIL and ADMIN_PASSWORD to .env
- docker-compose up

- docker exec -it flask-app /bin/bash
  - python manage.py db upgrade
  - python manage.py setup_dev
- Open http://127.0.0.1:5000/ 
  - Log in with ADMIN_EMAIL and ADMIN_PASSWORD




# Run postgres istance

docker run --name postgres-container -e POSTGRES_PASSWORD=secretPassword -e POSTGRES_USER=dev -e POSTGRES_DB=app-db -p 5432:5432 -d postgres

# Flask migrate

Inizialize migration `flask db init`
Commit migration `flask db migrate -m ""`

Apply migrations `flask db upgrade`

https://github.com/hack4impact/flask-base


If there are some trubles with "psycopg2" remove it from requirements.txt and use docker instead
