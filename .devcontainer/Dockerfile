FROM mcr.microsoft.com/devcontainers/python:3

# Selenium用にGoogle Chromeをaptで入れられる設定を入れる。
# ただし、aptでGoogle Chromeを入れるとエラーが発生するので手動で入れる
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -Lks https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y\
    peco\
    silversearcher-ag\
    vim\
    default-jdk\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
ARG HADOLINT_URL
RUN curl -Lk -o /usr/local/bin/hadolint ${HADOLINT_URL}\
    && chmod o+x /usr/local/bin/hadolint

# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make\
    && chmod o+x diff-highlight\
    && ln -s /usr/share/doc/git/contrib/diff-highlight/diff-highlight /usr/local/bin

WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
