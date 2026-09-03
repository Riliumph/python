FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm AS toolchain
# hadolint
ARG HADOLINT_URL
RUN wget -q -O /usr/local/bin/hadolint ${HADOLINT_URL} &&\
    chmod +x /usr/local/bin/hadolint
# python
RUN pip completion --bash > /etc/bash_completion.d/pip
# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make

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

COPY --from=toolchain /usr/local/bin/hadolint /usr/local/bin/hadolint
COPY --from=toolchain /usr/share/doc/git/contrib/diff-highlight/diff-highlight /usr/local/bin/diff-highlight
COPY --from=toolchain /etc/bash_completion.d/pip /etc/bash_completion.d/pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# Supervisor
ARG UID
ARG GID
RUN groupadd -g ${GID} supervisor &&\
    useradd -l -u ${UID} -g supervisor supervisor &&\
    mkdir -p /var/run/supervisor &&\
    chmod -R o+wrx /var/run/supervisor &&\
    mkdir -p /var/log/supervisor &&\
    chmod -R o+wrx /var/log/supervisor

COPY --chown=supervisor:supervisor ./supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
RUN chmod 666 /etc/supervisor/conf.d/jupyter.conf
