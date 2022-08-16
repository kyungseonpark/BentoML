# Base Image
FROM python:3.8.13
# copy base application
#COPY ./BentoAPI /app
COPY requirements-bento.txt /tmp/requirements.txt
# install package
RUN pip install pip==21
RUN pip install -r /tmp/requirements.txt
# set BentoML home
ENV BENTOML_HOME /bentoml
# start FastAPI
CMD uvicorn BentoAPI:bentoml --host 0.0.0.0 --port 22124 --app-dir /app
