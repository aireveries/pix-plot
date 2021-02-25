FROM nvidia/cuda:10.1-cudnn7-devel

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
        ca-certificates \
        cmake \
        curl \
        git \
        libprotobuf-dev \
        ninja-build \
        protobuf-compiler \
        python3-dev \
        python3-opencv \
        sudo \
        unzip \
        wget

RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3.7 python3.7-dev
RUN rm -rf /var/lib/apt/lists/*
RUN ln -sv /usr/bin/python3.7 /usr/bin/python

WORKDIR /root/

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install

ENV PATH="/root/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && \
        python get-pip.py --user && \
        rm get-pip.py

RUN pip install --user tensorboard
RUN pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

ENV FORCE_CUDA="1"
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"

COPY requirements.txt .
RUN pip install --user -r requirements.txt
RUN jupyter nbextension enable --py widgetsnbextension
RUN pip install setuptools

COPY . .
RUN python setup.py install
RUN pip install pycocotools==2.0.2