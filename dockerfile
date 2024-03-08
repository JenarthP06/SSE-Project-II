FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

ENV FLASK_APP=api/app.py
# ENV FLASK_ENV=development

CMD ["/usr/bin/supervisord", "flask", "run", "--host=0.0.0.0", "--port=5000"]