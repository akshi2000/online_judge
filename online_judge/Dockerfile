# pull official base image
FROM jrei/systemd-ubuntu:latest

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . /usr/src/app/

RUN apt update
RUN apt install python3 python3-pip -y

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]