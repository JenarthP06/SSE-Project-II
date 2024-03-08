FROM python:3.9

WORKDIR /api

COPY . .

# COPY .env /api

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

CMD ["/usr/bin/supervisord"]
