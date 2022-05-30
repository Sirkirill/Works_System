# Works_System
Test task

### to create and activate venv
```
python3 -m venv venv
source venv/bin/activate
```

### to create requirements.txt 
```
pip freeze > requirements.txt
```

### to install everything from requirements.txt
```
pip install -r requirements.txt
```
### I am not sharing database now. Create your own one. All this information will be hidden.

### to install postgre
```
sudo apt-get install postgresql postgresql-server-dev
```
### start configuring database and user
```
create user kirill with password 'kirill';
alter role kirill set client_encoding to 'utf8';
alter role kirill set default_transaction_isolation to 'read committed';
alter role kirill set timezone to 'UTC';
create database work_system owner kirill;
```
### database PostgreSQL
```
'ENGINE': ''django.db.backends.postgresql'',
'NAME': 'work_system',
'USER': 'kirill',
'PASSWORD': 'kirill',
'HOST': '127.0.0.1',
'PORT': '5432',
```
### Also you need to create .env file
```
SECRET_KEY='your secret key'
DEBUG=True
```

### To create and apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```
### Run server
```
python manage.py runserver
```
##### For test first task - runserver, at start page upload csv file. Current db will be show below
##### Also, you can test first task by django command
```
python manage.py collect_work path/to/your/file
```
##### For the second task go to url '/works/some_existed_iswc' where you can se result
