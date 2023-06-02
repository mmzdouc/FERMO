FROM python:3.8-slim-buster

COPY ./FERMO usr/src/FERMO/

WORKDIR /usr/src/FERMO

RUN pip install --upgrade pip
RUN pip install -e .

EXPOSE 8001

ENTRYPOINT ["python", "src/fermo/app.py"] 
