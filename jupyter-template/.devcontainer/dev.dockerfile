FROM python:latest

RUN apt-get update \
    && apt-get install --no-install-recommends -y\
    wget\
    peco\
    silversearcher-ag\
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*
# hadolint for docker
ARG HADOLINT_URL
RUN wget --progress=dot:giga -O /bin/hadolint ${HADOLINT_URL} --no-check-certificate
# jupyuter notebook
WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# New user
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN groupadd -g 1000 docker\
    && useradd -l -u 1000 -g docker -G sudo -m -s /bin/bash docker\
    && echo 'docker:docker' | chpasswd\
    && echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker
RUN printf "PS1='\u@\h(\$(hostname -i)):\w \n\\$ '" >> ~/.bashrc
WORKDIR /workspace

ENTRYPOINT [ "jupyter", "notebook", "--no-browser", "--allow-root"]
