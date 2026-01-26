#
# Docker Container for
# Jupyter Notebook Server
#
# Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

FROM pythoncontainer

MAINTAINER yves

VOLUME /notebooks
WORKDIR /notebooks

ENV PW jupyter
ENV PORT 9000

ADD notebook.sh /
RUN chmod u+x /notebook.sh

ADD jup_cert.pem /root/.ipython/profile_default/
ADD ipython_notebook_config.py /root/.ipython/profile_default/
ADD /ipynbs/* /notebooks/

CMD /notebook.sh PW PORT
