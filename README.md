To get everything up and running with Docker:

docker-compose up --build

If you need to shutdown, apply docker-compose down -v to delete volumes and create new database.

To get everything up and running with vitual environment:

flask --debug run --host=0.0.0.0  --port=8080
