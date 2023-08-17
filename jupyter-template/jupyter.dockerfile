FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# jupyterの実行
# ネットワーク系、認証系のオプションはcompose側で制御する。
ENTRYPOINT [ "jupyter", "notebook", "--no-browser", "--allow-root"]
