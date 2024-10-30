FROM ubuntu:23.10

RUN apt-get update
RUN apt-get upgrade

# Common tools
RUN apt-get install -y wget curl git

# g++
RUN apt-get install -y build-essential gcc g++ gdb

# Boost
RUN apt-get install -y libboost-all-dev

# Open3D
RUN apt-get install -y libopen3d-dev

COPY ./docker/ubuntu/install-cmake.sh /install-cmake.sh
COPY ./docker/ubuntu/setup.sh /setup.sh

ENTRYPOINT ["sh", "/setup.sh"]
