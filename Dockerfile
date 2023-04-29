FROM python:3
WORKDIR /eanet
COPY requirements.txt /eanet/
RUN pip install -r requirements.txt
COPY . /eanet/
