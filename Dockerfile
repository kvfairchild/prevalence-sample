FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    sudo \
    git \
    wget \
    python3 \
    python3-numpy \
    python3-pip \
    python3-scipy \
    && apt-get clean

RUN git clone https://github.com/kvgallagher/prevalence-sample && \
    cd prevalence-sample/model_data && \
    wget https://raw.githubusercontent.com/mit-quest/covid-health-management-system/master/json_model_interfaces/simulation_sample_jsons/prevalence-0_samples.json?token=ADRALN2QUQSPVVZUNGSQ3ES6X3PKC && \
    mv prevalence-0_samples.json?token=ADRALN2QUQSPVVZUNGSQ3ES6X3PKC prevalence-0_samples.json && \
    cd .. && mkdir ~/output