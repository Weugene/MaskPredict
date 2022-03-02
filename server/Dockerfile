FROM python:3.7
RUN mkdir /server
COPY requirements.txt /server/
WORKDIR /server
RUN ls /server
RUN pip3 install -r requirements.txt --no-cache-dir
