# events_manager

Events manager task


# Author
[Maciej Zięba \<maciekz82@gmail.com\>](https://github.com/maciekz)


## Installation

Create a python virtualenv and activate it (Python 3.11 is recommended):

```
python -m venv venv
source ./venv/bin/activate
```

Install application and its dependencies:

```
pip install -e .
```

You can also install the application with various development tools:

```
pip install -e .[dev]
```

Run required database migrations:

```
python src/manage.py migrate
```


## Running application

To run the application, use the standard Django `runserver` command:

```
python src/manage.py runserver
```

When using the default port `8000`, the following API endpoints are available:

 * http://localhost:8000/api/register/ - [POST] Registering a user
 * http://localhost:8000/api/token/ - [POST] Generate `access` and `refresh` tokens
 * http://localhost:8000/api/token/refresh/ - [POST] Refresh `access` token using `refresh` token
 * http://localhost:8000/api/events - [GET] List all events
 * http://localhost:8000/api/events/my_list - [GET] List events created by the current user
 * http://localhost:8000/api/events/ - [POST] Create new event
 * http://localhost:8000/api/events/<<pk:int>> - [GET] Event details
 * http://localhost:8000/api/events/<<pk:int>>/ - [PATCH] / [PUT] Edit event (possible only for the creator af the event)
 * http://localhost:8000/api/events/<<pk:int>>/registration/ - [POST] Register to an event
 * http://localhost:8000/api/events/<<pk:int>>/registration/ - [DELETE] Unregister from an event
