# pull official base image
FROM python:3.8.3-alpine

# set work directory
ENV APP=/usr/src/app
RUN mkdir $APP
WORKDIR $APP

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # install Pillow dependencies
    && apk add jpeg-dev zlib-dev libjpeg \
    # install Cryptography dependencies
    && apk add libressl-dev musl-dev libffi-dev openssl-dev cargo


# install dependencies
RUN pip install --upgrade pip
COPY ./local.requirements.txt .
RUN pip install -r local.requirements.txt

# copy entrypoint.local.sh
COPY ./config/docker/entrypoint.local.sh ./config/docker/
RUN sed -i 's/\r$//g' $APP/config/docker/entrypoint.local.sh
RUN chmod +x $APP/config/docker/entrypoint.local.sh


# copy project
COPY . .

# run entrypoint.local.sh
ENTRYPOINT ["/usr/src/app/config/docker/entrypoint.local.sh"]
