FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y\
    peco\
    silversearcher-ag\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
ARG HADOLINT_URL
RUN wget --progress=dot:giga -O /usr/local/bin/hadolint ${HADOLINT_URL} --no-check-certificate\
    && chmod o+x /usr/local/bin/hadolint

# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make\
    && chmod o+x diff-highlight

# New user
USER 1000
