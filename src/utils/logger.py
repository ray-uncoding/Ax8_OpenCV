import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO, console_output=True, max_bytes=5 * 1024 * 1024, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 檔案處理器
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 控制台處理器
    if console_output:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(name)s - %(levellevel)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger