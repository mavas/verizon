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
RUN aptitude install -y protobuf-compiler
RUN aptitude install -y youtube-dl git

RUN useradd -ms /bin/bash verizon
USER verizon
WORKDIR /home/verizon
RUN python3 -c "import cv2; print(cv2.__version__)"
RUN python3 -c "import youtube_dl; print(youtube_dl.version.__version__)"
RUN pip install --upgrade pip
RUN python3 -c "import cv2; print(cv2.__version__)"
RUN python3 -c "import youtube_dl; print(youtube_dl.version.__version__)"

RUN git clone https://github.com/mavas/verizon
RUN git clone https://github.com/tensorflow/models
RUN cd models/research && \
    protoc object_detection/protos/*.proto --python_out=. && \
    cp object_detection/packages/tf2/setup.py . && \
    python3 -m pip install .

ENV PYTHON_2_ENV py2env
ENV PYTHON_3_ENV py3env

RUN wget --quiet -O ~/miniconda.sh \
    http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -f && \
    #~/miniconda.sh -b -f -p $DATALAB_CONDA_DIR && \
    rm ~/miniconda.sh && \
    conda update conda --quiet --yes && \
    conda config --system --append channels conda-forge && \
    conda config --system --set show_channel_urls true && \
    conda update --all --quiet --yes && \
    conda create --yes --quiet --name $PYTHON_3_ENV python=3.8 tensorflow

#COPY --chown=verizon tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl .
#RUN pip install --user ./tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl
#RUN python3 -c "import tensorflow as tf; print(tf.__version__)"

#ENTRYPOINT 
CMD ["echo", "love"]
