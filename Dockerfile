FROM python:3.8

ENV DIRECTORY /neubility/control_server
WORKDIR ${DIRECTORY}
COPY . ${DIRECTORY}/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000 60066
