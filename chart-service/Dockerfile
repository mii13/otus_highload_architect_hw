FROM python:3.10.1-bullseye

RUN apt-get update && \
    apt-get install -y \
    bash curl net-tools zip unzip \
    jq dnsutils iputils-ping


RUN mkdir -p /data/db /etc/consul.d


ADD https://releases.hashicorp.com/consul/1.4.4/consul_1.4.4_linux_amd64.zip /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

ADD https://github.com/mattn/goreman/releases/download/v0.0.10/goreman_linux_amd64.zip /tmp/goreman.zip
RUN cd /bin && unzip /tmp/goreman.zip && chmod +x /bin/goreman && rm /tmp/goreman.zip

ADD ./consul /etc/consul.d
ADD Procfile /root/Procfile

ADD consul.sh /opt


COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

EXPOSE 8088

ENTRYPOINT [ "goreman" ]
CMD [ "-f", "/root/Procfile", "start" ]