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

COPY start.sh bot-execution.sh requirements.txt bot/* /code/
RUN chmod +x /code/start.sh /code/bot-execution.sh

RUN pip install --no-cache-dir -r /code/requirements.txt
RUN mkdir /output

CMD ["/code/start.sh"] 
