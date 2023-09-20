### Installation 
## Create a virtual envelope 
python3 -m venv .venv

## Activate the virtual envelope
source .venv/bin/activate

## Install requirements
cd leominsterphilosopers
pip3 install -r requirements

## Create the database
flask --app lp shell
db.drop_all()
db.create_all()

## Test using unit_tests
flask --app lp test

## Run
flask --app lp run --debug

## Using flask-migrate
# Create a migration repository
flask db init
# Perform the initial migration
flask db migrate -m "Initial migration."
# Apply the changes
flask db upgrade
# Help
flask db --help
