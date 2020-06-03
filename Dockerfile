FROM python:3.8.2-slim-buster

RUN apt-get update \
    && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY bin/* src/* requirements.txt /app/
RUN chmod +x /app/container-startup.sh /app/tweetbrief-execution.sh

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN mkdir /output

CMD ["/app/container-startup.sh"] 
