FROM nikolaik/python-nodejs:python3.6-nodejs12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY ./package.json ./package-lock.json ./
RUN npm install

RUN apt-get update && apt-get install -yqq libpq-dev

COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --deploy --system

ENV DJANGO_SETTINGS_MODULE "rating.settings.prod"

COPY ./entrypoint.sh ./
COPY ./src ./src/
RUN chmod +x entrypoint.sh

WORKDIR /app/src/

ENTRYPOINT ["/app/entrypoint.sh"]
