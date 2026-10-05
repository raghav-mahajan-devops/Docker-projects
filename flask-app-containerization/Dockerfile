FROM python:3.11

WORKDIR /flask-app

COPY . /flask-app

RUN pip install -r requirements.txt

ENTRYPOINT ["python","run.py"]
