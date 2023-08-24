from typing import Union
from pathlib import Path
from functools import cache
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from render_code.utils.file import check_template_file
from render_code.conf import settings


@cache
def create_jinja_loader_for_file(file: Union[str, Path]):
    file = check_template_file(file)
    loader = FileSystemLoader(file.parent)
    return loader


@cache
def create_jinja_env_for_file(file: Union[str, Path]):
    file = check_template_file(file)
    loader = create_jinja_loader_for_file(file)
    env = Environment(loader=loader)
    env.variable_start_string = settings.JINJA_VARIABLE_START_STRING
    env.variable_end_string = settings.JINJA_VARIABLE_END_STRING
    env.add_extension("jinja2.ext.loopcontrols")
    return env
