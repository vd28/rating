## Deployment
1. You need to install `docker` and `docker-compose` before deployment.

2. Go to the `./docker/prod` directory.

3. Create `.env.db` file with the following content:

    ```
    POSTGRES_USER=<user name>
    POSTGRES_PASSWORD=<database password>
    POSTGRES_DB=<database name>
    ```

4. Create `.env.web` file with the following content:

    ```
    SECRET_KEY=<long and hard to guess string>
    DATABASE_URI=postgres://<user name>:<database password>@db:5432/<database name>
    TIME_ZONE=UTC
    ```
   Replace **UTC** with your time zone.

5. Run `docker-compose up -d --build`.

6. Create superuser if not already created:
    
    1. jump into container using command `docker-compose exec web bash`;
    2. run `python manage.py createsuperuser`;
    3. follow prompted instructions.
    
7. Optionally populate database with initial data:

    1. jump into container using command `docker-compose exec web bash`;
    2. run `python manage.py loaddata initial`.

8. Server will listen on http://0.0.0.0:1337
