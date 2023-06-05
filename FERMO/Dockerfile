FROM python:3.8-slim-buster

COPY ../ home/FERMO/

WORKDIR /home/FERMO

RUN pip install --upgrade pip
RUN pip install -e .

EXPOSE 8001

ENTRYPOINT ["gunicorn", "app:app"]
