FROM python:3.12.4-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ /usr/src/app

RUN python -m pip install .

ENTRYPOINT ["analyzer"]