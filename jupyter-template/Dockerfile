FROM python:latest

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
WORKDIR /workspace

ENTRYPOINT [ "jupyter", "notebook", "--no-browser", "--allow-root"]
