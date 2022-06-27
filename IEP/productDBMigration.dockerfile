FROM python:3

RUN mkdir -p /opt/src/daemon-migration
WORKDIR /opt/src/daemon-migration

COPY daemon/migrate.py ./migrate.py
COPY daemon/configuration.py ./configuration.py
COPY models.py ./models.py
COPY daemon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

# ENTRYPOINT ["echo", "hello world"]
# ENTRYPOINT ["sleep", "1200"]
ENTRYPOINT ["python", "./migrate.py"]
