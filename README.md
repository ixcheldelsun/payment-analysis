To get everything up and running with Docker:

docker-compose up --build

If you need to shutdown, apply docker-compose down -v to delete volumes and create new database.

To get everything up and running with vitual environment:

python3 -m venv venv

pip install -r requirements.txt

source venv/bin/activate

python3 app/server.py

Swagger documentation can be found in the /apidocs/ endpoint.


