# FlaskProject

This is the internet, web and cloud exam project, developed in flask

# Run postgres istance

docker run --name postgres-container -e POSTGRES_PASSWORD=secretPassword -e POSTGRES_USER=dev -e POSTGRES_DB=app-db -p 5432:5432 -d postgres
