FROM python:3.11-slim-buster

ENV INSTALL_PATH /fermo_gui
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY ./fermo_gui .

RUN pip install --upgrade pip
RUN pip install hatch
RUN hatch -v env create

EXPOSE 8001

CMD hatch run gunicorn "fermo_gui:create_app()" --bind "0.0.0.0:8001"