# Aegir
This project is a simple beer delivery app backend using python and postgres, implemented to test my software engineering skills. [Aegir](https://en.wikipedia.org/wiki/%C3%86gir) is the name of Norse mythology, associated with beer and parties.

## Development notes
- I am using postgres + postgis to save and handle with geo localization.
- SQLAlchemy and GeoAlchemy as ORM to query and manipulate data.  

## How to configure to local development
1. Create and activate virtual env
2. Install dependencies
3. Make your magic! :)
4. Execute tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
tox
```

## How to execute managements commands
1. Install Aegir tool on your virtual environment.
2. Call aegir command to see a list with all commands.

```bash
pip install .
aegir
``` 

### List of management commands
- db create: Create database structure.
- pdvs load <file_name>: Not implemented.
- shell: Open an interactive python shell with Aegir context. 
