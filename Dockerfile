FROM nikolaik/python-nodejs:python3.6-nodejs12

RUN apt-get update && apt-get install -yqq netcat

WORKDIR /app/

COPY ./package.json ./package-lock.json ./
RUN npm install

RUN apt-get update && apt-get install -yqq libpq-dev

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --deploy --system

ENV DJANGO_SETTINGS_MODULE "rating.settings.prod"

COPY ./entrypoint.sh ./
RUN chmod +x entrypoint.sh
COPY ./src ./src/

WORKDIR /app/src/

ENTRYPOINT ["/app/entrypoint.sh"]
