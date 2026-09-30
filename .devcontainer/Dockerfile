FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm AS toolchain
# docker
ARG DOCKER_URL="https://download.docker.com/linux/debian"
ARG DOCKER_KEY_PATH="/etc/apt/keyrings/docker.asc"
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get -qq update &&\
    apt-get -qq -y install --no-install-recommends \
    ca-certificates \
    gnupg
RUN curl -fsSL "${DOCKER_URL}/gpg" -o "${DOCKER_KEY_PATH}"; \
    chmod a+r "${DOCKER_KEY_PATH}"; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=${DOCKER_KEY_PATH}] ${DOCKER_URL} $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list;
RUN apt-get -qq update &&\
    apt-get -qq -y install --no-install-recommends \
    ## Docker-outside-of-Docker
    ## Need not install docker process
    # containerd.io \
    # docker-ce \
    docker-ce-cli \
    docker-buildx-plugin \
    docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*
RUN docker completion bash > /etc/bash_completion.d/docker

WORKDIR /tmp
# hadolint
ARG HADOLINT_URL="https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64"
RUN curl -fsSL ${HADOLINT_URL} -o hadolint  &&\
    install -m 755 hadolint /usr/local/bin/hadolint
# python
RUN pip completion --bash > /etc/bash_completion.d/pip
# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make && \
    install -m 755 diff-highlight /usr/local/bin/diff-highlight

# ======================================================================

FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

RUN DEBIAN_FRONTEND=noninteractive\
    apt-get -qq update &&\
    apt-get -qq install --no-install-recommends -y \
    # utility
    peco\
    ripgrep\
    silversearcher-ag\
    vim\
    # networks
    dnsutils\
    iputils-ping\
    # for container
    supervisor\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

COPY --from=toolchain /usr/local/bin /usr/local/bin
COPY --from=toolchain /etc/bash_completion.d /etc/bash_completion.d

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Supervisor
ARG UID
ARG GID
RUN groupadd -g ${GID} supervisor &&\
    useradd -l -u ${UID} -g supervisor supervisor &&\
    install -d --owner=supervisor --group=supervisor /var/run/supervisor &&\
    install -d --owner=supervisor --group=supervisor /var/log/supervisor

COPY --chown=supervisor:supervisor ./supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
