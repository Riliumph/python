FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Selenium用にGoogle Chromeをaptで入れられる設定を入れる。
# ただし、aptでGoogle Chromeを入れるとエラーが発生するので手動で入れる
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -Lks https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends -y\
    # utility
    peco\
    silversearcher-ag\
    vim\
    # networks
    dnsutils\
    iputils-ping\
    # for container
    supervisor\
    default-jdk\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
ARG HADOLINT_URL
RUN curl -Lks -o /usr/local/bin/hadolint ${HADOLINT_URL}\
    && chmod o+x /usr/local/bin/hadolint

# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make\
    && chmod o+x diff-highlight\
    && ln -s /usr/share/doc/git/contrib/diff-highlight/diff-highlight /usr/local/bin

WORKDIR /etc/bash_completion.d
RUN pip completion --bash > pip

WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -q -r requirements.txt

# Supervisor
COPY --chown=:supervisor --chmod=666 ./supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
RUN groupadd -g 2000 supervisor\
    && mkdir -p /var/run/supervisor\
    && chmod -R o+wrx /var/run/supervisor\
    && chmod -R o+wrx /var/log/supervisor

