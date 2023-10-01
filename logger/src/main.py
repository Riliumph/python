import logging.config
import json


# ログ設定を定義します
with open('config.json', 'r') as config_file:
    log_config = json.load(config_file)

# ログ設定を適用します
logging.config.dictConfig(log_config)

# ロガーを取得します
logger = logging.getLogger()

# ログを書き出します
logger.info("これは情報ログです。")
logger.error("これはエラーログです。")
