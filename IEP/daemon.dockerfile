FROM python:3

RUN mkdir -p /opt/src/daemon
WORKDIR /opt/src/daemon

COPY daemon/application.py ./application.py
COPY daemon/configuration.py ./configuration.py
COPY models.py ./models.py
COPY daemon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/daemon"

ENTRYPOINT ["python", "./application.py"]
