# Reads the /var/log/auth.log file and prints the number of failed login attempts

import re
from collections import defaultdict

# sudo grep preauth /var/log/auth.log | grep -v grep
FILE = "/var/log/auth.log"

# [preauth] is in all failed login attempts
PATTERNS = ["preauth"]

# GOOD login = "Accepted publickey" or "Accepted password"

names: dict[str, int] = defaultdict(int)
ips: dict[str, int] = defaultdict(int)

ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
user_pattern = re.compile(r" user (\w+) ")


def main():
    with open(FILE) as f:
        for line in f:
            if any(pattern in line for pattern in PATTERNS):
                match_ip = ip_pattern.search(line)
                if match_ip:
                    ips[match_ip.group()] += 1

                match_name = user_pattern.search(line)
                if match_name:
                    names[match_name.group(1)] += 1

    print("Names:")
    names_sorted = sorted(names.items(), key=lambda x: x[1])
    for name, count in names_sorted:
        print(f"{name}: {count}")

    print("IPs:")
    ips_sorted = sorted(ips.items(), key=lambda x: x[1])
    for ip, count in ips_sorted:
        print(f"{ip}: {count}")

    print("Total failed login attempts:", sum(ips.values()))


if __name__ == "__main__":
    main()
