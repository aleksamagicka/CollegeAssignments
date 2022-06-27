FROM python:3

RUN mkdir -p /opt/src/warehouse
WORKDIR /opt/src/warehouse

COPY warehouse/application.py ./application.py
COPY warehouse/configuration.py ./configuration.py
COPY models.py ./models.py
COPY warehouse/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/warehouse"

ENTRYPOINT ["python", "./application.py"]
