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