FROM python:3

RUN mkdir -p /opt/src/customer
WORKDIR /opt/src/customer

COPY customer/application.py ./application.py
COPY customer/configuration.py ./configuration.py
COPY models.py ./models.py
COPY customer/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/customer"

ENTRYPOINT ["python", "./application.py"]
