# Aegir
This project is a simple beer delivery app backend using python and postgres, implemented to test my software engineering skills. [Aegir](https://en.wikipedia.org/wiki/%C3%86gir) is the name of Norse mythology, associated with beer and parties.

## Development notes
- I am using postgres + postgis to save and handle with geo localization.
- I did not used a project boilerplate. The structure and files was creates considering my experience with other frameworks (Django, Flask, etc) and some lessons learned with past mistakes.
- [SQLAlchemy](https://www.sqlalchemy.org/) and [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/) as ORM to query and manipulate data.
- [Tornado](https://www.tornadoweb.org/en/stable/) to create the RESTful api and serve it.  

## How to execute managements commands
1. Create and activate virtual env
1. Install Aegir tool on your virtual environment.
2. Configure your local instance using .env file
3. Call aegir command to see a list with all commands.

```bash
python -m venv .venv && source .venv/bin/activate
pip install .
cp contrib/env.sample .env
python aegir
``` 

### List of management commands
- db create: Create database structure.
- pdvs load <file_path>: Load given json data to database.
- shell: Open an interactive python shell with Aegir context.
- runserver: Execute http server. 

## How to configure to local development
1. Create and activate virtual env
2. Install dependencies
3. Configure your local instance, using .env file.
4. Create the database (see "How to execute managements commands" section)
5. Make your magic! :)
6. Execute tests

```bash
python -m venv .venv && source .venv/bin/activate
cp contrib/env.sample .env
python aegir db create
pip install -r requirements-dev.txt
tox
```

## How to load test data
1. With Aegir installed (see "How to execute managements commands") and database created, execute the fallowing command.

```bash
python aegir pdvs load <json file path (see sample at contri/data.sample.json)>
```

## Running the server
1. With Aegir installed (see "How to execute managements commands") and database created, execute the server.
```bash
python aegir runserver
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
