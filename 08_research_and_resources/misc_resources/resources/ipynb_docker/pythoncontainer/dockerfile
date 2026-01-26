# Docker Container with
# Basic Python Install
# 
# Dr. Yves J. Hilpisch
# The Python Quants GmbH

FROM ubuntu:trusty

MAINTAINER yves

ADD install.sh /
RUN chmod u+x /install.sh
RUN /install.sh
ENV PATH /root/miniconda/bin:$PATH

CMD ["/bin/bash"]
