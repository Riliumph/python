FROM mcr.microsoft.com/devcontainers/base:2-debian12 AS toolchain
ARG HADOLINT_URL
RUN wget -q -O hadolint ${HADOLINT_URL} && chmod +x hadolint
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make

FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

RUN apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends -y \
    # utility
    peco\
    silversearcher-ag\
    vim\
    # networks
    dnsutils\
    iputils-ping\
    # for container
    supervisor\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
COPY --from=toolchain /hadolint /usr/local/bin/hadolint
# git
COPY --from=toolchain /usr/share/doc/git/contrib/diff-highlight/diff-highlight /usr/local/bin/diff-highlight

RUN pip completion --bash > /etc/bash_completion.d/pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -q -r requirements.txt

# Supervisor
ARG UID
ARG GID
RUN groupadd -g ${GID} supervisor \
    && useradd -l -u ${UID} -g supervisor supervisor \
    && mkdir -p /var/run/supervisor \
    && chmod -R o+wrx /var/run/supervisor \
    && chmod -R o+wrx /var/log/supervisor

COPY --chown=supervisor:supervisor ./supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
RUN chmod 666 /etc/supervisor/conf.d/jupyter.conf

