from pathlib import Path
from typing import Union
from render_code.core.template import create_jinja_env_for_file
from render_code.utils.schema import expand_schema
from render_code.utils.file import check_schema_file, check_template_file
from render_code.conf import constants
from inspect import getmembers
import os
import glob


def render_file(template_file: Union[str, Path], schema_file: Union[str, Path]) -> str:
    template_file = check_template_file(template_file)
    schema_file = check_schema_file(schema_file)

    env = create_jinja_env_for_file(template_file)
    template = env.get_template(template_file.name)
    data = expand_schema(schema_file)

    config = {
        **{
            name: member
            for name, member in getmembers(constants)
            if not name.startswith("__")
        }
    }
    content = template.render(data=data, config=config)
    return content


def render_dir(
    directory: Union[str, Path], output: Union[str, Path] = None, include: str = None
) -> bool:
    if isinstance(directory, str):
        directory = Path(directory)
    if isinstance(output, str):
        output = Path(output)

    if not directory.exists():
        print(f"{directory} is not exists.")
        return False
    if not output.exists():
        print(f"{output} is not exists.")
        return False

    directory = directory.expanduser()
    output = output.expanduser()

    for root, dirs, files in os.walk(directory):
        root = Path(root)
        for _dir in dirs:
            _dir = root / _dir
            files = _dir.glob(include) if include else _dir.iterdir()
            for file in files:
                if not file.suffix == ".tpl":
                    continue
                stem = file.stem.split(".")[0]
                schema_file = _dir / f"{stem}.json"
                content = render_file(file, schema_file)
                output_file = output / _dir.relative_to(directory) / file.stem
                if not output_file.parent.exists():
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(content)

    return True
