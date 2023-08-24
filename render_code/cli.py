import click
from pathlib import Path
from typing import Union
from render_code.utils.file import check_schema_file, check_template_file
from render_code.core import render
from render_code.conf import settings

SUFFIXS = settings.TEMPLATE_SUFFIXS


@click.group(help="This tool helps generate code based on schema and templates.")
def commands():
    pass


@click.command()
@click.option(
    "--template-file",
    "-t",
    required=True,
    help=f"Code template file, supports files with {'|'.join(SUFFIXS)} suffix.",
)
@click.option(
    "--schema-file",
    "-s",
    required=False,
    help="Json file that contains the data needed to render the code template.",
)
@click.option(
    "--output",
    "-o",
    required=False,
    help="Output the result to the specified file, if None, print to standard output.",
)
def render_file(template_file: Union[Path, str], schema_file: Union[Path, str] = None, output: str = None):
    """Specify file to render.

    Examples::

        render-code render-file --help
    """
    template_file = check_template_file(template_file)
    if schema_file is None:
        stem = template_file.stem.split('.')[0]
        schema_file = template_file.parent / f"{stem}.json"
    schema_file = check_schema_file(schema_file)
    content = render.render_file(template_file, schema_file)

    if output is None:
        print(content)
        return

    output = Path(output)
    if not output.exists():
        raise FileNotFoundError(f"{output} not found.")

    if output.is_dir():
        output = output / template_file.stem

    output = output.expanduser()
    output.write_text(content, encoding="utf-8")


@click.command()
@click.option(
    "--directory",
    "-d",
    required=True,
    help="The directory to render code templates.",
)
@click.option(
    "--output",
    "-o",
    required=False,
    help="Output the result to the specified directory, if None, output to same directory as template.",
)
@click.option(
    "--include",
    "-i",
    required=False,
    help="Template files matched by glob.",
)
def render_dir(
    directory: str, output: str = None, include: str = None
):
    """Specify directory to render.

    Examples::

        render-code render-dir --help
    """
    directory = Path(directory)
    if not directory.exists():
        print(f'{directory} is not exists.')
        return
    if output is None:
        output = directory
    else:
        output = Path(output)
    if not output.exists():
        output.mkdir(parents=True, exist_ok=True)

    result = render.render_dir(directory, output, include)
    if not result:
        print('fail')
    else:
        print('done')


@click.command()
def render_here():
    """Render templates in the current directory.

    Examples::

        render-code render-here --help
    """
    cwd = Path.cwd()
    render.render_dir(cwd)


commands.add_command(render_file)
commands.add_command(render_dir)
commands.add_command(render_here)

if __name__ == "__main__":
    commands()

"""debug cases
python -m render_code.cli --help
python -m render_code.cli render-dir --help
python -m render_code.cli render-file -t ./examples/base/models.py.tpl -o ./examples/base
python -m render_code.cli render-dir -d ./examples/render-dir
python -m render_code.cli render-dir -d ./examples/render-dir -o ./var/tmp/render-dir
python -m render_code.cli render-dir -d ./examples/render-dir -o ./var/tmp/render-dir -i **/a.txt.tpl
"""
