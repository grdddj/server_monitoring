import logging
import os
import time
from typing import Iterator


# TODO: could do some tests of functionality
def yield_file_lines(file_path: str, logger: logging.Logger) -> Iterator[str]:
    """Monitor /var/log/auth.log for new login attempts and authentications, accounting for log rotation."""
    start_from_beginning = False
    last_known_size = 0

    try:
        while True:
            logger.info(
                {
                    "event": "MonitoringFileStarted",
                    "file": file_path,
                    "start_from_beginning": start_from_beginning,
                }
            )
            with open(file_path, "r") as file:
                if not start_from_beginning:
                    # Initially, move to the end of the file
                    file.seek(0, 2)
                    last_known_size = os.path.getsize(file_path)

                while True:
                    current_size = os.path.getsize(file_path)
                    if current_size < last_known_size:
                        # File was truncated/rotated, restart the file watching
                        start_from_beginning = True
                        logger.info(
                            {
                                "event": "FileRotated",
                                "file": file_path,
                                "size": current_size,
                                "last_known_size": last_known_size,
                            }
                        )
                        last_known_size = 0
                        break
                    last_known_size = current_size

                    line = file.readline().strip()
                    if not line:
                        time.sleep(0.1)  # Wait for new content
                        continue

                    yield line
    except FileNotFoundError:
        logger.error({"event": "FileNotFound", "file": file_path})
    except PermissionError:
        logger.error({"event": "PermissionError", "file": file_path})
