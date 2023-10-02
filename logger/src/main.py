import logging.config
import json

# ログ設定を定義します
with open('config.json', 'r') as config_file:
    log_config = json.load(config_file)

# ログ設定を適用します
logging.config.dictConfig(log_config)

# ロガーを取得します
app_logger = logging.getLogger("app")
sys_logger = logging.getLogger("sys")

# ログを書き出します
app_logger.info("APP:これは情報ログです。")
app_logger.error("APP:これはエラーログです。")
sys_logger.info("Sys:これは情報ログです。")
sys_logger.error("Sys:これはエラーログです。")
