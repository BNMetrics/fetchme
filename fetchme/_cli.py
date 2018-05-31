import click

import os
import subprocess

from configparser import NoOptionError
from bnmutils import ConfigParser
from bnmutils.exceptions import InvalidConfigOption

from .utils import _get_config_path, _set_commands
from .__version__ import __version__


DEFAULT_COMMANDS = ['edit', 'set', 'remove']


@click.version_option(__version__, '--version', '-v', '-V')
@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    *Entry point*

    Examples:

        - To edit the config file in editor:

            $ fetchme edit

        - To set an alias to a command:

            $ fetchme set ssh="ssh -i /path/to/my/key/file usrname@123.43.678.678"

        - To execute the above set command:

            $ fetchme ssh

        - To remove the command

            $ fetchme remove ssh

    Help options:

        - Call 'help' commands(This also displays available commands):

            $ fetchme -h

            $ fetchme --help

        - Check version:

            $ fetchme -v

    """


@cli.command()
@click.pass_context
def edit(ctx):
    """
    Command for editing '.fetchmerc' file in an editor, default editor: vim
    """
    config_path = _get_config_path()
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
    """
    Command for setting an alias to a long command

    :argument: content: key=value, e.g: ssh="ssh -i /path/to/my/key/file usrname@123.43.678.678"

    :option: --override, -o: option for overriding existing key

    :raises: ValueError, if the alias with provided name has already being set in .fetchmerc file
    """
    name, val = content.split('=', 1)

    if name in DEFAULT_COMMANDS:
        raise ValueError(F"'{name}' is a default command, and it cannot be set!")

    config_path = _get_config_path()
    config = ConfigParser.from_files(config_path)

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
    """
    Commands for removing a set alias

    :param: name: The name of the alias, defined in .fetchmerc file

    :raises: ValueError: if such alias does not exist
    """
    config_path = _get_config_path()
    config = ConfigParser.from_files(config_path)

    try:
        config.get('fetchme', name)
    except NoOptionError:
        raise InvalidConfigOption(f"'{name}' is not a valid config option. Avalables: {config.options('fetchme')}")

    config.remove_option('fetchme', name)

    with config_path.open('w') as file:
        config.write(file)


_set_commands(cli)
