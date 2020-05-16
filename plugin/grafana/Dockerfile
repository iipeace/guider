FROM ubuntu:18.04
MAINTAINER Yoonje Choi <yoonje.choi.dev@gmail.com>

ENV ARCH amd64

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

# Default versions
ENV INFLUXDB_VERSION 1.7.10
ENV GRAFANA_VERSION  6.6.2

# Clear previous sources
RUN rm /var/lib/apt/lists/* -vf

RUN apt-get -y update && \
 apt-get -y dist-upgrade && \
 apt-get -y install \
  apt-utils \
  ca-certificates \
  curl \
  git \
  htop \
  gnupg \
  libfontconfig \
  mysql-client \
  mysql-server \
  nano \
  net-tools \
  supervisor \
  wget \
  adduser \
  libfontconfig1 && \
 curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
 apt-get install -y nodejs

# Configure Supervisord and base env
COPY supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /root

RUN mkdir -p /var/log/supervisor && rm -rf .profile

COPY bash/profile .profile

# Install InfluxDB
RUN wget https://dl.influxdata.com/influxdb/releases/influxdb_${INFLUXDB_VERSION}_${ARCH}.deb && \
	dpkg -i influxdb_${INFLUXDB_VERSION}_${ARCH}.deb && rm influxdb_${INFLUXDB_VERSION}_${ARCH}.deb

# Configure InfluxDB
COPY influxdb/influxdb.conf /etc/influxdb/influxdb.conf

# Install Grafana
RUN wget https://dl.grafana.com/oss/release/grafana_${GRAFANA_VERSION}_amd64.deb && \
	dpkg -i grafana_${GRAFANA_VERSION}_amd64.deb && rm grafana_${GRAFANA_VERSION}_amd64.deb

# Configure Grafana
COPY grafana/grafana.ini /etc/grafana/grafana.ini

# Cleanup
RUN apt-get clean && \
 rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["/usr/bin/supervisord"]