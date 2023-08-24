from render_code.conf import settings
from typing import Union
from pathlib import Path
from functools import cache


@cache
def check_template_file(file: Union[str, Path]) -> Path:
    if isinstance(file, str):
        file = Path(file)

    if not file.exists() or file.suffix not in settings.TEMPLATE_SUFFIXS:
        suffixs = "|".join(settings.TEMPLATE_SUFFIXS)
        raise FileNotFoundError(
            f"{file} is not a valid template file, it must be a file with the {suffixs} suffix."
        )

    return file.expanduser()


@cache
def check_schema_file(file: Union[str, Path]) -> Path:
    if isinstance(file, str):
        file = Path(file)

    if not file.exists() or file.suffix != ".json":
        raise FileNotFoundError(
            f"{file} is not a valid schema file, it must be a json file."
        )
    return file.expanduser()
