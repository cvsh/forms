
#!/bin/bash

echo "Installing requirements.py"
pip install -r requirements.txt

echo "Running server"
uvicorn main:app --reload
