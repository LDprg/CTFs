FROM ubuntu@sha256:d22e4fb389065efa4a61bb36416768698ef6d955fe8a7e0cdb3cd6de80fa7eec

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd

RUN useradd -m ctf
WORKDIR /home/ctf

RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /usr/bin/timeout /home/ctf/bin

COPY ./config/ctf.xinetd /etc/xinetd.d/ctf
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

COPY ./service/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

COPY ./src/attachment /home/ctf/attachment

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    touch /home/ctf/flag && \
    chmod 744 /home/ctf/flag

# EXPOSE 9999

ENTRYPOINT ["/bin/bash","/docker-entrypoint.sh"]
