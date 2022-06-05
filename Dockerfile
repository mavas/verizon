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
RUN aptitude install -y ffmpeg libopencv-dev python3-opencv libprotoc-dev
RUN aptitude install -y libprotoc23
RUN aptitude install -y youtube-dl git

RUN useradd -ms /bin/bash verizon
USER verizon
WORKDIR /home/verizon

RUN git clone https://github.com/mavas/verizon
RUN python3 -c "import cv2; print(cv2.__version__)"
RUN python3 -c "import youtube_dl; print(youtube_dl.version.__version__)"
RUN git clone https://github.com/tensorflow/models
RUN cd models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . python3 -m pip install
