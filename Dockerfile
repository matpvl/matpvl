# syntax=docker/dockerfile:1

# use official slim Python image
FROM python:3.12-slim

# maintainer of the docker image
LABEL maintainer="matpvl"

# see logs immediately
ENV PYTHONUNBUFFERED=1


WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync

# copy the rest of the source code
COPY . .

# omit the default CMD for now