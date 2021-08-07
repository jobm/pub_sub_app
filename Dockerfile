# This is a simple Dockerfile to use while developing
# It's not suitable for production

FROM python:3.9.6-buster
RUN mkdir /delivery_app
WORKDIR /delivery_app
COPY . /delivery_app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python",  "app.py"]
