FROM python:3.11.4-slim

ENV PYTHONUNBUFFERED 1

# New user
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG USERNAME=django
RUN groupadd -g 1000 ${USERNAME}\
    && useradd -l -u 1000 -g ${USERNAME} -G sudo -m -s /bin/bash ${USERNAME}\
    && echo "${USERNAME}:${USERNAME}" | chpasswd\
    && echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /opt/django/
# volumeは実行時に張られるためコピーが必要
COPY requirements.txt /opt/django/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
