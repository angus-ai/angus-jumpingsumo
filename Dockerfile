FROM debian:jessie

RUN apt-get update
RUN apt-get upgrade

RUN apt-get install -y git wget automake autoconf libtool yasm nasm python unzip openjdk-7-jdk libssl-dev make libncurses5-dev virtualenv

RUN mkdir -p /root/SDK

RUN cd /root/SDK; git clone https://github.com/ARDroneSDK3/ARSDKBuildUtils.git

RUN cd /root/SDK/ARSDKBuildUtils/; ./SDK3Build.py -t Unix -j 4; exit 0;

RUN cd /root/SDK; git clone https://github.com/angus-ai/angus-jumpingsumo.git

RUN cd /root/SDK/angus-jumpingsumo; make

RUN mkdir /root/.angusdk

ADD config.json /root/.angusdk/config.json
ADD certificate.pem /root/.angusdk/certificate.pem

RUN virtualenv /root/SDK/angus-jumpingsumo/env
RUN . /root/SDK/angus-jumpingsumo/env/bin/activate; pip install angus-sdk-python

RUN . /root/SDK/angus-jumpingsumo/env/bin/activate; cd /root/SDK/angus-jumpingsumo; 

ENV PYTHONPATH $PYTHONPATH:/root/SDK/angus-jumpingsumo/env
ENV PATH /root/SDK/angus-jumpingsumo/env/bin:$PATH

WORKDIR /root/SDK/angus-jumpingsumo

CMD ["python", "wrapper.py"]


