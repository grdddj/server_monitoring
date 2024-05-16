import re
import time
from pathlib import Path
from typing import TypedDict

from common import yield_file_lines
from config import load_config
from logger import get_json_logger
from notify import send_pushbullet_message

logger = get_json_logger(Path(__file__).with_suffix(".log"))

FILE = "/var/log/auth.log"

password_pattern = "Accepted password for"

# Accepted publickey for user from 1.2.3.4 port
login_pattern = re.compile(
    r"Accepted publickey for (\w+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)

# Connection closed by invalid user user 1.2.3.4 port 46010 [preauth]
unauthorized_pattern = re.compile(
    r" user (\w+) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*preauth"
)

last_messages: dict[str, float] = {}


class Event(TypedDict):
    event: str
    name: str
    ip: str


def send_message_deduplicate(title: str, event: Event, seconds: int) -> None:
    user_name = event["name"]
    user_ip = event["ip"]
    last_message = last_messages.get(user_name, 0)
    now = time.time()
    if now - last_message > seconds:
        last_messages[user_name] = now
        text = f"{user_name} from {user_ip}"
        send_pushbullet_message(title, text)


def monitor_and_report() -> None:
    for line in yield_file_lines(FILE, logger=logger):
        try:
            analyze_line(line)
        except Exception as e:
            logger.error({"event": "Error", "message": str(e)})


def analyze_line(line: str) -> None:
    if password_pattern in line:
        send_pushbullet_message("ERROR: Password login detected", line)
        logger.warning(line)

    match_login = login_pattern.search(line)
    if match_login:
        config = load_config()

        name: str = match_login.group(1)
        ip: str = match_login.group(2)
        if ip not in config.known_ips:
            event: Event = {
                "event": "UnknownIPAddressLogin",
                "name": name,
                "ip": ip,
            }
            logger.warning(event)
            send_message_deduplicate(
                f"{config.server_name} - WARNING: unknown IP",
                event,
                config.deduplicate_seconds,
            )
        else:
            event = {
                "event": "KnownIPAddressLogin",
                "name": name,
                "ip": ip,
            }
            logger.info(event)
            send_message_deduplicate(
                f"{config.server_name} login",
                event,
                config.deduplicate_seconds,
            )

    match_unauthorized = unauthorized_pattern.search(line)
    if match_unauthorized:
        event = {
            "event": "UnauthorizedLoginAttempt",
            "name": match_unauthorized.group(1),
            "ip": match_unauthorized.group(2),
        }
        logger.warning(event)


if __name__ == "__main__":
    logger.info({"event": "MonitoringStarted"})
    monitor_and_report()
