
#!/bin/bash

echo "Creating virtual env"
python3 -m venv mvenv
source mvenv/bin/activate

echo "Installing requirements.py"
pip install -r requirements.txt

echo "Running server"
uvicorn main:app --reload
