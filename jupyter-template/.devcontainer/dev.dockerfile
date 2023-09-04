FROM python:latest

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y\
    wget\
    peco\
    silversearcher-ag\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
ARG HADOLINT_URL
RUN wget --progress=dot:giga -O /usr/local/bin/hadolint ${HADOLINT_URL} --no-check-certificate\
    && chmod +x /usr/local/bin/hadolint

# jupyter notebook
WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# New user
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG USERNAME=devcontainer
RUN groupadd -g 1000 ${USERNAME}\
    && useradd -l -u 1000 -g ${USERNAME} -G sudo -m -s /bin/bash ${USERNAME}\
    && echo "${USERNAME}:${USERNAME}" | chpasswd\
    && echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER 1000
RUN printf "PS1='\[\$(tput setaf 4)\]\u\[\$(tput sgr0)\]@\[\$(tput setaf 2)\]\h(\$(hostname -i))\[\$(tput sgr0)\]:\[\$(tput setaf 3)\]\w\\n\[\$(tput sgr0)\]\\$ '" >> ~/.bashrc
WORKDIR /workspace

ENTRYPOINT [ "jupyter", "notebook", "--no-browser", "--allow-root"]
