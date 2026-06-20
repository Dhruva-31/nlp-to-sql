import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/queries.log")


def log_query(data: dict):

    LOG_FILE.parent.mkdir(exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(json.dumps(data))

        f.write("\n")
