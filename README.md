##To get everything up and running with Docker:

docker-compose up --build

If you need to shutdown, apply docker-compose down -v to delete volumes and create new database.

##To get everything up and running with vitual environment:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cd app && gunicorn app:app

##Documentation

Swagger documentation can be found in the /apidocs/ endpoint.


