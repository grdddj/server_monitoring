import re
from pathlib import Path

from common import yield_file_lines
from logger import get_json_logger

logger = get_json_logger(Path(__file__).with_suffix(".log"))

FILE = "/var/log/syslog"

ufw_block_ip_port_pattern = re.compile(
    r" \[UFW BLOCK\] .* SRC=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* DPT=(\d+) "
)


def monitor() -> None:
    for line in yield_file_lines(FILE, logger=logger):
        try:
            analyze_line(line)
        except Exception as e:
            logger.error({"event": "Error", "message": str(e)})


def analyze_line(line: str) -> None:
    match = ufw_block_ip_port_pattern.search(line)
    if match:
        ip = match.group(1)
        port = match.group(2)
        # TODO: add a possibility to conditionally block the IP (when it makes a lot of requests, or request to a specific port, etc.)
        # TODO: find out a flood of requests from the same IP and block it
        event = {
            "event": "UFWBlock",
            "ip": ip,
            "port": port,
        }
        logger.warning(event)


if __name__ == "__main__":
    logger.info({"event": "MonitoringStarted"})
    monitor()
