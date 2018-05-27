import click

import os
import subprocess

from logme.config import read_config
from configparser import NoOptionError

from .utils import get_config_path, set_commands
from .__version__ import __version__


DEFAULT_COMMANDS = ['edit', 'set']


@click.version_option(__version__, '--version', '-v', '-V')
@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    Entry point


    """


@cli.command()
@click.pass_context
def edit(ctx):
    config_path = get_config_path()
    editor = os.environ.get('EDITOR', 'vim')

    if not config_path.exists() and not config_path.is_file():
        raise FileNotFoundError(f"{config_path.resolve()} does not exist, please reinstall or upgrade the package.")

    subprocess.call([editor, str(config_path)])


@cli.command()
@click.argument('content', required=1)
@click.option('--override', '-o',
              help='override an existing',  is_flag=True)
@click.pass_context
def set(ctx, content, override):
    name, val = content.split('=', 1)

    if name in DEFAULT_COMMANDS:
        raise ValueError(F"'{name}' is a default command, and it cannot be set!")

    config_path = get_config_path()
    # TODO: possibly extract to a common 'config_utils' repo
    config = read_config(config_path)

    try:
        config.get('fetchme', name)
        if not override:
            raise ValueError(f"'{name}' already exist! use --override, or -o flag to override")
    except NoOptionError:
        pass

    config['fetchme'][name] = val

    with config_path.open('w') as file:
        config.write(file)


@cli.command()
@click.argument('name', required=1)
@click.pass_context
def remove(ctx, name):
    pass


set_commands(cli)

