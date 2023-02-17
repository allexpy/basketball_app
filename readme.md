# Steps to run and test the application

1. Create `.env.dev` file at the ROOT of the project containing `RAPID_API_KEY`. E.g. `RAPID_API_KEY = 7456764754747hgkjhkghkdhgdfhf` and django `SECRET_KEY` E.g. `SECRET_KEY = 48gy85bn4589`
1. Create a virtualenv using poetry and install dependencies: `poetry install`
2. Activate the virtualenv. To find the path of the poetry virtualenv use `poetry env info`. Lastly use `source venv/bin/path-to-virtualenv-python`.
3. `./manage.py makemigrations`
4. `./manage.py migrate`
5. `./manage.py runserver`
6. To create 1 admin user and 1 normal user directly use: `./manage.py loaddata initial_users.json` otherwise you 
can create an admin user by calling `./manage.py create_admin` and register a normal user at: http://localhost:8000/api/account/sign_up/

7. To import necessary data for tests:
- `./manage.py import_countries`
- `./manage.py import_season`
- `./manage.py import_leagues`
- `./manage.py import_teams`


Due to the huge amount of requests needed to import all teams, only a few a teams will be imported from league 5, country: USA.

# Testing
You can manually test endpoints in postman or access the openapi endpoint http://localhost:8000/api/swagger/.

### 1. Register normal user:

- Endpoint: http://localhost:8000/api/account/sign_up/
- Method: POST
- Example JSON: 
```
{
  "email": "user@example.com",
  "password1": "pAssw0rd!",
  "password2": "pAssw0rd!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login (admin/user)

- Endpoint: http://localhost:8000/api/account/log_in/
- Method: POST
- Example JSON: `{
    "email": "admin@example.com",
    "password": "pAssw0rd!"
}`
- Example response: 
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjcwNjgyMiwiaWF0IjoxNjc2NjIwNDIyLCJqdGkiOiJkOGViOWFhZjMyYzg0MzRiYjg3YzM3Mjg4NTk3M2VhOSIsImlkIjoxLCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiZmlyc3RfbmFtZSI6bnVsbCwibGFzdF9uYW1lIjpudWxsfQ.LmQOJxlNGqvgqquLxeu56QGUZekiKrYQ_1powjx8Ggk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NjI0MDIyLCJpYXQiOjE2NzY2MjA0MjIsImp0aSI6Ijk1NjBkM2U2Njc4NTRmYWQ4NzE4MmI4MTdiZmFmNzIwIiwiaWQiOjEsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjpudWxsLCJsYXN0X25hbWUiOm51bGx9.42_iEuhM_avws0vl3c4gpG-QAWZwkEHKzDGqzT0Xx2c"
}
```


- Info: Access token expires after an hour.
- To access the rest of the endpoints you need to be authenticated by using Bearer <Your Access API key> in the Authorization Header.

### 3. To refresh the token

- Endpoint: http://localhost:8000/api/account/token/refresh/
- Method: POST
- Example JSON: 
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjQ1ODMzMiwiaWF0IjoxNjc2MzcxOTMyLCJqdGkiOiI3N2MzYzNiNzMwOWU0MGE1YWRkMDRjYzM5NzM3OWIyOSIsImlkIjo1LCJlbWFpbCI6InRlc3QxMjNAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkpvaG4iLCJsYXN0X25hbWUiOiJEb2UifQ.QAP5-33igr4Mewa552_as7mL6gkz_TuHBqn32ET-6LI"
}
```

- Example response: 
```
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NjI0MDIyLCJpYXQiOjE2NzY2MjA0MjIsImp0aSI6Ijk1NjBkM2U2Njc4NTRmYWQ4NzE4MmI4MTdiZmFmNzIwIiwiaWQiOjEsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjpudWxsLCJsYXN0X25hbWUiOm51bGx9.42_iEuhM_avws0vl3c4gpG-QAWZwkEHKzDGqzT0Xx2c"
}
```

### 4. Access data endpoints

- Endpoint: http://localhost:8000/api/data/countries/
- Headers: {}
- Methods to use: GET/POST/PUT/PATCH/DELETE
- Example response from list: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "reference_id": 75,
            "code": "TM",
            "name": "Turkmenistan"
        }
    ]
}
```


- Endpoint: http://localhost:8000/api/data/seasons/
- Methods to use: GET/POST/PUT/PATCH/DELETE
- Example response from list: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 16,
            "year": 2023,
            "period": "2022-2023",
        }
    ]
}
```


- Endpoint: http://localhost:8000/api/data/leagues/
- Methods to use: GET/POST/PUT/PATCH/DELETE
- Example response from list: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "reference_id": 284,
            "name": "World Cup Women",
            "type": "League",
            "country": 62,
            "season": 15
        }
    ]
}
```


- Endpoint: http://localhost:8000/api/data/teams/
- Methods to use: GET/POST/PUT/PATCH/DELETE
- Example response from list: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "reference_id": 284,
            "name": "World Cup Women",
            "type": "League",
            "country": 62,
            "season": 15
        }
    ]
}
```


### 5. Manage normal user country permissions

- Endpoint: http://localhost:8000/api/account/users/2/
- Method: PATCH
- Example JSON: `{
    "countries": [5]
}`
- Example response: 
```
{
    "id": 2,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "countries": [
        {
            "id": 5,
            "reference_id": 5,
            "code": "US",
            "name": "USA"
        }
    ]
}
```
- #### Info: If you remove a country from a users permissions, all games assigned to that user for the respective country will be unassigned from him.


### 6. Import games

- Endpoint: http://localhost:8000/api/games/import-games/
- Method: POST
- Example JSON: 
```
{
    "league": "178",
    "season": "2022"
}
```
- #### INFO: Import games using this league and season, it will match with the imported teams.
- Example response: 
```
{
    "success": true
}
```


### 7. Users accessing assigned and unassigned games and assigning them to themselves

- Endpoint: http://localhost:8000/api/games/user/assigned/
- Method: GET
- Example response: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 116,
            "user": 2,
            "country": 5,
            "reference_id": 318089,
            "league": 2290,
            "season": 15,
            "home_team": 20,
            "away_team": 18,
            "datetime": "2022-08-21T21:00:00Z",
            "status": "Game Finished",
            "scores": {
                "home": {
                    "quarter_1": null,
                    "quarter_2": 25,
                    "quarter_3": null,
                    "quarter_4": 26,
                    "over_time": null,
                    "total": 51
                },
                "away": {
                    "quarter_1": null,
                    "quarter_2": 21,
                    "quarter_3": null,
                    "quarter_4": 14,
                    "over_time": null,
                    "total": 35
                }
            }
        }
    ]
}
```


- Endpoint: http://localhost:8000/api/games/user/unassigned/
- Method: GET
- Example response: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 116,
            "user": null,
            "country": 5,
            "reference_id": 318089,
            "league": 2290,
            "season": 15,
            "home_team": 20,
            "away_team": 18,
            "datetime": "2022-08-21T21:00:00Z",
            "status": "Game Finished",
            "scores": {
                "home": {
                    "quarter_1": null,
                    "quarter_2": 25,
                    "quarter_3": null,
                    "quarter_4": 26,
                    "over_time": null,
                    "total": 51
                },
                "away": {
                    "quarter_1": null,
                    "quarter_2": 21,
                    "quarter_3": null,
                    "quarter_4": 14,
                    "over_time": null,
                    "total": 35
                }
            }
        }
    ]
}
```


- Endpoint: http://127.0.0.1:8000/api/games/user/unassigned/116/assign-game/
- Method: GET
- Example response: 
```
{
    "success": True
}
```


# Running tests

At the root of the project call `pytest`.

# Code quality checking

At the root of the project call `isort . --profile black`, `black .` and `flake8 .`