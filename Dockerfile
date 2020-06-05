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

COPY scripts/. tweetbrief/. Pipfile Pipfile.lock /app/
WORKDIR /app

RUN chmod +x container-startup.sh tweetbrief-execution.sh
RUN pip install --no-cache-dir pipenv
RUN pipenv lock --requirements > requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

CMD ["/app/container-startup.sh"] 
