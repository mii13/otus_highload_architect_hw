FROM centos:7.5.1804

# FROM debian:bullseye


RUN yum update -y && \
 	yum -y install git ncurses-devel make cmake gcc-c++ boost boost-devel wget unzip nano bzip2 mysql-devel mysql-lib
# RUN apt update -y && \
# 	apt install -y git ncurses-devel make cmake gcc-c++ boost boost-devel wget unzip nano bzip2 mysql-devel mysql-lib
#

RUN git clone https://github.com/tarantool/mysql-tarantool-replication.git && cd mysql-tarantool-replication && git submodule update --init --recursive


WORKDIR mysql-tarantool-replication
RUN cmake . && make

RUN cp replicatord /usr/local/sbin/replicatord


COPY ./replicatord.yml /usr/local/etc/replicatord.yml
COPY ./init.sh /init.sh
RUN chmod +x /init.sh

CMD ["/init.sh"]

# CMD ["sleep", "300000"]


