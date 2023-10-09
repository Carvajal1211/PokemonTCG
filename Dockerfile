FROM ubuntu:20.04
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN export PATH="$PATH:~/.yarn/bin"


RUN mkdir /code
WORKDIR /code

ADD ./conf/requirements.txt /code/
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends build-essential 
RUN apt-get -y install python3-pip

RUN apt-get -y install wget
RUN apt-get -y install libmysqlclient-dev
RUN apt install -y unzip

RUN pip install --upgrade pip
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y pkg-config
RUN pip install -r requirements.txt

ADD ./ /code/

ARG DJANGO_APP
ENV DJANGO_APP=${DJANGO_APP}
EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 ${DJANGO_APP}.wsgi:application"]