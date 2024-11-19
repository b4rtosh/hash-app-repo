FROM dizcza/docker-hashcat:latest

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev libpq-dev netcat
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

WORKDIR /app/cryptoapp

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
#
#CMD ["python", "cryptoapp/manage.py", "runserver", "0.0.0.0:8000"]