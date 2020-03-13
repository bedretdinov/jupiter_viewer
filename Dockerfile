FROM python:3.6-jessie

LABEL maintainer="asd "

WORKDIR /app


# expect a build-time variable
RUN sed -i '/jessie-updates/d' /etc/apt/sources.list \
&&   apt-get update  \
&&   apt-get install -y \
&&   apt-get install -y mysql-client \
&&   apt-get -y install python3-pip \
&&   pip3 install jupyter \
&&   pip3 install pyquery \
&&   pip3 install Flask==1.0.2 \
&&   pip3 install -U clickhouse-sqlalchemy \
&&   pip3 install clickhouse-driver==0.0.16  \
&&   pip3 install numpy==1.15.3 \
&&   pip3 install pandas==0.23.4 \
&&   pip3 install urllib3==1.22 \
&&   pip3 install requests==2.18.4 \
&&   pip3 install pymysql  \
&&   pip3 install peewee   \
&&   pip3 install plotly==4.5.4 \
&&   pip3 install matplotlib

COPY . /app

CMD python3 /app/main.py
