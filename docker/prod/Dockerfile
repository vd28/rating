FROM nikolaik/python-nodejs:python3.6-nodejs12

WORKDIR /app/

RUN apt-get update && apt-get install -yqq netcat libpq-dev

COPY ./package.json ./package-lock.json ./
RUN npm install

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --deploy --system

COPY ./docker/prod/entrypoint.sh ./
RUN chmod +x entrypoint.sh
COPY ./src ./src/

WORKDIR /app/src/

ENV DJANGO_SETTINGS_MODULE "rating.settings.prod"

ENTRYPOINT ["/app/entrypoint.sh"]
