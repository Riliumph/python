FROM debian:bookworm-slim


RUN apt-get update &&\
    apt-get install --no-install-recommends -y \
    postgresql-client-15=15.3-0+deb12u1 &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*
