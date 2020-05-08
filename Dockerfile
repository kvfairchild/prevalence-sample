FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    sudo \
    git \
    python3-numpy \
    python3-pip \
    python3-scipy \
    && apt-get clean

RUN git clone https://github.com/kvgallagher/prevalence-sample && \
    cd prevalence-sample