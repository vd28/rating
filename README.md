## Deployment
1. Install **docker** and **docker-compose** before deployment.

2. Create **.env.db** file in project root and with following content:

    ```
    POSTGRES_USER=<user name>
    POSTGRES_PASSWORD=<database password>
    POSTGRES_DB=<database name>
    ```

3. Create **.env.web** file in project root with following content:

    ```
    SECRET_KEY=<long and hard to guess string>
    DATABASE_URI=postgres://<database name>:<database password>@db:5432/<database name>
    ```

4. Run `docker-compose up -d --build` in project root.

5. Create superuser if not already created:
    1. jump into container using command `docker-compose exec web bash`;
    2. run `python manage.py createsuperuser`;
    3. follow prompted instructions.

6. Server will listen on http://localhost:1337
