FROM python:3.10-slim

RUN apt-get update -q \
    && apt-get install --no-install-recommends -qy \
    gcc musl-dev \
    inetutils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /apps/core

COPY require.txt /apps/core/require.txt
RUN pip3 install -r /apps/core/require.txt --no-cache-dir
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg