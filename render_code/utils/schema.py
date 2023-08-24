from pathlib import Path
import json


def expand_schema(file: Path) -> dict:
    content = file.read_text()
    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError:
        data = {}
    return data
