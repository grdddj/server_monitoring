import subprocess
import time
from pathlib import Path
from typing import Set

from config import load_config
from logger import get_json_logger

logger = get_json_logger(Path(__file__).with_suffix(".log"))
config = load_config()


def get_recent_logins() -> Set[str]:
    """Fetch the recent login records using the `last` command."""
    output = subprocess.check_output(["last", "-w"]).decode("utf-8")
    return set(output.splitlines())


def monitor_logins(interval: int):
    """Monitor for new logins every `interval` seconds."""
    known_logins = get_recent_logins()

    while True:
        time.sleep(interval)
        current_logins = get_recent_logins()

        new_logins = current_logins - known_logins
        if new_logins:
            for login in new_logins:
                if "still logged in" not in login:
                    continue
                # user    pts/4        1.2.3.4     Sat Apr  6 22:37   still logged in
                name = login.split()[0]
                ip = login.split()[2]
                logger.info(
                    {
                        "event": "NewLogin",
                        "name": name,
                        "ip": ip,
                    }
                )

        known_logins = current_logins


if __name__ == "__main__":
    logger.info(
        {
            "event": "MonitorLogins",
            "interval": config.login_interval_seconds,
        }
    )
    monitor_logins(config.login_interval_seconds)
