FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get -y install apt-utils
RUN apt-get -y install aptitude
RUN aptitude update -y
RUN aptitude safe-upgrade -y
RUN aptitude install -y build-essential python3 python3-pip cmake g++ python3-numpy-dev python3-dev python3-venv
RUN aptitude install -y python3-arrow python3-cloudpickle ipython3 cython3
RUN aptitude install -y ffmpeg libopencv-dev python3-opencv
RUN aptitude install -y gradle gradle-plugin-protobuf

RUN useradd -ms /bin/bash verizon
USER verizon
WORKDIR /home/verizon
#COPY --chown=verizon vimrc .vimrc
RUN git clone https://github.com/mavas/verizon
