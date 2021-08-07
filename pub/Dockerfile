# This is a simple Dockerfile to use while developing
# It's not suitable for production

FROM python:3.9.6-alpine
RUN mkdir /coordinates_pub
WORKDIR /coordinates_pub
COPY ./pub/pub_coordinates.py ./extensions.py ./pub/__init__.py ./

ENV PATH="${PATH}:/root/.local/bin"
RUN python -m pip install --upgrade pip
RUN pip install redis==3.5.3


CMD ["python",  "pub_coordinates.py"]
