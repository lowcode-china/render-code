from pathlib import Path

TEMPLATE_SUFFIXS = (
    ".tpl",
    ".jinja",
)

JINJA_VARIABLE_START_STRING = "{{"
JINJA_VARIABLE_END_STRING = "}}"

BASE_DIR = Path(__file__).parent.parent

CWD = Path.cwd()