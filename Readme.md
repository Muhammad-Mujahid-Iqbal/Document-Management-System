# Document Management System

This is a sample python application having REST APIs to manage documents data including metadata for documents and their statuses

# Pre Requisite

1. Python 3.7 or greater
2. Postgres and PGAdmin (To view data)


# Start Backend Server

Install virtualenv first (to create a python virtual environment)


```
# Creating virtual environment (Go to the code folder)
python -m venv /path/to/new/virtual/environment

# Activating virtual environment
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# DB Configuration
In postgres, create a db with name 'DMS' for user postgres
You can modify the .env file further if face connectivity issues

```

Run Server
```
# Go to the code folder
cd <code_folder>

# Run Database migrations (migration file already created)
alembic upgrade head

# Run Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run API documentation
http://localhost:8000/docs

```


# API documentation

After starting the server go to the link

http://localhost:8000/docs


# Sample Application Usage

Follow the instructions to use the application logically


```
1. Call Users Post API and create a user. This user will be used
   to authenticate API calls as JWT Authentication is applied.
2. Create a Customer using customers Post API to register a new    
   customer. You can create as many users as you want. They 
   have unique UUID. Use this customer ID in later APIs.
3. Now create document metadata and document status using their
   respective POST APIs separatily. CustomerID and documentID 
   entered must be unique combination.
4  Now call Document Summary APIs to see calculated results for 
   given customerID 
```

# Test Cases
Run test-cases with following commands (old data will be deleted)
```
pytest # Run without showing print in code.


pytest -s # Run and show prints inside code.
```