FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    python3-numpy \
    python3-pip \
    python3-scipy \
    && apt-get clean

RUN wget https://github.com/kvgallagher/prevalence-sample && \
    cd prevalence-sample