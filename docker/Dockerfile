ARG MANUAL_IMAGE_TAG="latest"

FROM python:3.6-stretch
LABEL maintainer="PolySwarm Developers <info@polyswarm.io>"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py README.md LICENSE ./
COPY src src
COPY test test

RUN pip install .
