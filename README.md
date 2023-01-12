##To get everything up and running with Docker:

docker-compose up --build

If you need to shutdown, apply docker-compose down -v to delete volumes and create new database.

##To get everything up and running with vitual environment:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

mysql -uroot < db/init.sql (Para crear las tablas en la base de datos)

PD: si necesitan volver a levantarla deben de correr los comandos  mysql -uroot -e "DROP user test@localhost" y  mysql -uroot -e "DROP DATABASE test"

cd app && gunicorn app:app

##Documentation

Swagger documentation can be found in the /apidocs/ endpoint.


