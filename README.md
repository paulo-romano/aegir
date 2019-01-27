# Aegir
This project is a simple beer delivery app backend using python and postgres, implemented to test my software engineering skills. [Aegir](https://en.wikipedia.org/wiki/%C3%86gir) is the name of Norse mythology, associated with beer and parties.

## Development notes
- I am using postgres + postgis to save and handle with geo localization.
- I did not used a project boilerplate. The structure and files was creates considering my experience with other frameworks (Django, Flask, etc) and some lessons learned with past mistakes.
- [SQLAlchemy](https://www.sqlalchemy.org/) and [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/) as ORM to query and manipulate data.
- [Tornado](https://www.tornadoweb.org/en/stable/) to create the RESTful api and serve it.

## How to configure docker services
In file docker-compose.yaml, you will find a service called "api", in this service has a environment key with all variables needed to run this service. For test propose, you should keep it unchanged.

## How to execute using docker and docker-compose
1. Install docker and docker compose. You can find instructions to install on ubuntu 18.04 linux in [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) (Docker) and [this](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04) (Docker compose). You can chose a different version and linux distribution in posts page.
2. Configure docker services (See "How to configure docker services" section).
3. Build the images and services.
4. Start services in background.
5. If is the first time, you should create the database. Obs.: Wait to postgres services start completely, a.k.a, "database system is ready to accept connections" log entry.

```bash
docker-compose build
docker-compose up -d
docker-compose run api python -m aegir db create
```  

## How to execute managements commands
1. Call aegir command to see a list with all commands.

```bash
docker-compose run api python -m aegir
``` 

### List of management commands
- db create: Create database structure.
- pdvs load <file_path>: Load given json data to database.
- shell: Open an interactive python shell with Aegir context.
- runserver: Execute http server. 

## How to load test data
1. With Aegir installed (see "How to execute managements commands") and database created, execute the fallowing command.

```bash
docker-compose run api python -m aegir pdvs load <json file path (see sample at contri/data.sample.json)>
```

### Creating a new PDV using REST
```bash
curl -X POST \
  http://127.0.0.1:8000/api/pdv \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
  "pdvs": [ 
    {
        "id": 1, 
        "tradingName": "Adega da Cerveja - Pinheiros",
        "ownerName": "Zé da Silva",
        "document": "1432132123891/0001",
        "coverageArea": { 
          "type": "MultiPolygon", 
          "coordinates": [
            [[[30, 20], [45, 40], [10, 40], [30, 20]]], 
            [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
          ]
        },
        "address": { 
          "type": "Point",
          "coordinates": [-46.57421, -21.785741]
        }
    }
  ]
}'
```

### Get PDV by ID
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/pdv?id=62e7a718-7ddb-4497-97e7-69133f7c8801' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
```

### Find all PDVs by coverage area
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/pdv?lat=<LAT>>&lng=<LONG>' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
```

## How to configure to local development
1. Create and activate virtual env
2. Install dependencies
3. Configure your local instance, using .env file.
4. Install Aegir on virtual env.
4. Create the database.
5. Make your magic! :)
6. Execute tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install . --editable
cp contrib/env.sample .env
python -m aegir db create
pip install -r requirements-dev.txt
tox
```

## How to deploy
1. Install Ubuntu 18.04 on remote machine. A guide to DigitalOcean droplet can be found [here](https://www.digitalocean.com/docs/droplets/how-to/create/).
2. Change deploy script to be executable.
3. Execute the deploy script. If you do not have configured your ssh key, it will prompt for remote password twice.
```bash
chmod +x contrib/deploy.sh
USER=root HOST=206.189.203.139 sh contrib/deploy.sh
```

## Running the local server
1. With Aegir installed and database created (see "How to configure to local development"), execute the server.
```bash
python -m aegir runserver
```
