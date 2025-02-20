FROM python:3.12-slim-bullseye AS base
LABEL maintainer="0xChaser"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc g++ curl procps net-tools tini git

RUN addgroup --gid 1002 --system springboot_python_dev && \
    adduser --shell /bin/bash --disabled-password --uid 1002 --system springboot_python_dev

COPY pyproject.toml /app/pyproject.toml

# Set up the Python environment
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip wheel

RUN pip install uv

COPY . /app

SHELL ["/bin/bash", "-c"]

FROM base AS development
WORKDIR /app

# Install the project dependencies
RUN uv pip install --no-cache-dir -e .[dev]

ENTRYPOINT ["springboot_python"]
CMD ["dev"]

# Expose the application port
EXPOSE 8000

FROM base AS production
WORKDIR /app

RUN addgroup --gid 1001 --system springboot_python && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group springboot_python

USER springboot_python
WORKDIR /app

RUN uv pip install --no-cache-dir -e .

# Expose the application port
EXPOSE 8000

ENTRYPOINT ["run"]