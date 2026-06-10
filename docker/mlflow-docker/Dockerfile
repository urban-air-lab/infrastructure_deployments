FROM python:3.11-slim

# Install system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000