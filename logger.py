import json
import logging
from pathlib import Path
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        try:
            message_data = json.loads(message.replace("'", '"'))
            log_record: Dict[str, Any] = {
                "date": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                **message_data,
            }
        except Exception:
            log_record = {
                "date": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "message": message,
            }

        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def get_json_logger(file: str | Path) -> logging.Logger:
    logger = logging.getLogger(str(file))
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.FileHandler(file))
    json_formatter = JsonFormatter()
    for handler in logger.handlers:
        handler.setFormatter(json_formatter)
    return logger


if __name__ == "__main__":
    logger = get_json_logger(Path(__file__).with_suffix(".log"))
    logger.info("Test message")
    logger.info({"key": "value", "key2": "value2"})
