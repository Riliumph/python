FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y\
    peco\
    silversearcher-ag\
    vim\
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

# New user
USER 1000


# Completion for Bash 5.1.4(Resolve at Bash 5.2.1)
RUN { \
    echo "source /usr/share/bash-completion/completions/docker"; \
    pip completion --bash;\
    } >> ~/.bashrc
