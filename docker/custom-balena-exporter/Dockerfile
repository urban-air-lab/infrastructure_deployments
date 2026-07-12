FROM python:3.11-slim

# Install python packages
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY balena_exporter.py /app/balena_exporter.py
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "balena_exporter:app", "--host", "0.0.0.0", "--port", "8000"]
