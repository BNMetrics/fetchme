import subprocess
from pathlib import Path

import click

from logme.config import read_config


def get_config_path() -> Path:
    """
    Get the configuration file path
    """
    home = Path.home()

    return home / '.fetchmerc'


def set_commands(click_group: click.core.Group):
    """
    Set commands to click group based on the options in .fetchmerc file
    """
    config_path = get_config_path()
    config = read_config(config_path)

    option_names = config.options('fetchme')

    for i in option_names:
        func = get_command_func(i, config)

        click_group.command(name=i)(click.pass_context(func))


def get_command_func(name, config):

    def subcommand(ctx):
        commands = config.get('fetchme', name).split(' ')

        subprocess.call(commands)

    return subcommand
