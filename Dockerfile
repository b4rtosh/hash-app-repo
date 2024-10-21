FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    ocl-icd-libopencl1 \
    ocl-icd-dev \
    clinfo \
    git \
    rocm-dkms

RUN git clone https://github.com/hashcat/hashcat.git /opt/hashcat \
    && cd /opt/hashcat \
    && make install

RUN ln -s /opt/hashcat/hashcat.bin /usr/bin/hashcat

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "cryptoapp/manage.py", "runserver", "0.0.0.0:8000"]