## Deployment
1. Install **docker** and **docker-compose** before deployment.

2. Create **.env.db** file in project root with the following content:

    ```
    POSTGRES_USER=<user name>
    POSTGRES_PASSWORD=<database password>
    POSTGRES_DB=<database name>
    ```

3. Create **.env.web** file in project root with the following content:

    ```
    SECRET_KEY=<long and hard to guess string>
    DATABASE_URI=postgres://<user name>:<database password>@db:5432/<database name>
    TIME_ZONE=UTC
    ```
   Replace **UTC** with your time zone.

4. Run `docker-compose up -d --build` in project root.

5. Create superuser if not already created:
    
    1. jump into container using command `docker-compose exec web bash`;
    2. run `python manage.py createsuperuser`;
    3. follow prompted instructions.
    
6. Optionally populate database with initial data:

    1. jump into container using command `docker-compose exec web bash`;
    2. run `python manage.py loaddata initial`.

7. Server will listen on http://0.0.0.0:1337
