import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent

CONFIG_FILE = HERE / "config.json"


@dataclass
class Config:
    pushbullet_token: str
    deduplicate_seconds: int
    login_interval_seconds: int
    known_ips: list[str]
    server_name: str


def load_config() -> Config:
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        return Config(
            pushbullet_token=data["pushbullet_token"],
            deduplicate_seconds=data["deduplicate_seconds"],
            login_interval_seconds=data["login_interval_seconds"],
            known_ips=data["known_ips"],
            server_name=data["server_name"],
        )
