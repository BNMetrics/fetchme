import subprocess
from pathlib import Path
from functools import wraps

# Imports for type hinting
import click
from typing import Callable
from configparser import ConfigParser

from logme.config import read_config


def _get_config_path() -> Path:
    """
    Get '.fetchmerc' configuration file path
    """
    home = Path.home()

    return home / '.fetchmerc'


def _set_commands(click_group: click.core.Group):
    """
    Set commands to click group based on the options in .fetchmerc file
    """
    config_path = _get_config_path()
    config = read_config(config_path)

    option_names = config.options('fetchme')

    for i in option_names:
        func = _get_command_func(i, config)

        click_group.command(name=i)(click.pass_context(func))


def _get_command_func(name: str, config: ConfigParser) -> Callable:
    """
    Get the stub function for commands.
    allowing the click group to automatically take commands from '.fetchmerc' options

    :param name: name of the option in .fetchmerc
    :param config: configuration, ConfigParser object

    :return: callable function
    """
    command = config.get('fetchme', name)

    @doc_parametrize(name=name, command=command)
    def subcommand(ctx):
        """
        Execute command alias '{name}'; command: {command}
        """
        command_fields = command.split(' ')

        subprocess.call(command_fields)

    return subcommand


# TODO: Extract this to my common lib
def doc_parametrize(**parameters) -> Callable:
    """
    Decorator for allowing parameters to be passed into docstring

    :param parameters: key value pair that corresponds to the params in docstring
    """
    def decorator_(callable_):
        new_doc = callable_.__doc__.format(**parameters)
        callable_.__doc__ = new_doc

        @wraps(callable_)
        def wrapper(*args, **kwargs):
            return callable_(*args, **kwargs)

        return wrapper

    return decorator_


