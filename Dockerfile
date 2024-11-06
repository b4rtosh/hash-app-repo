FROM dizcza/docker-hashcat:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT []

CMD ["python", "cryptoapp/manage.py", "runserver", "0.0.0.0:8080"]