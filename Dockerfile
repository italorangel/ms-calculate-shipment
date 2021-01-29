FROM python:3.8.1-alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt

CMD ["chmod", "+x", "/usr/src/app/entrypoint.sh"]