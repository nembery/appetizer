
FROM registry.gitlab.com/panw-gse/as/as-py-base-image@sha256:b189d625a5386b7aff598d44e6822e02f0731e30061b890eaec68d658ac52e36

LABEL description="Skillet Appetizer"
LABEL version="0.7"
LABEL maintainer="tsautomatedsolutions@paloaltonetworks.com"

ENV CNC_USERNAME=paloalto
ENV CNC_PASSWORD=appetizer
ENV CNC_HOME=/home/cnc_user
ENV CNC_APP=appetizer
ENV GIT_SSL_NO_VERIFY="1"
ENV COLUMNS=80
ENV PYTHONHTTPSVERIFY=0

WORKDIR /app

RUN groupadd -g 998 docker && \
    usermod cnc_user -G docker,root

RUN git clone https://github.com/PaloAltoNetworks/pan-cnc.git /app/cnc && cd /app/cnc && git checkout develop && \
    git log --oneline -n1

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r cnc/requirements.txt && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install pydevd-pycharm~=203.7717.81

COPY appetizer /app/src/appetizer

RUN chmod +x /app/src/appetizer/start_app.sh && \
    chown cnc_user:cnc_group /app/src/appetizer

EXPOSE 8080
CMD ["/app/src/appetizer/app.sh"]
