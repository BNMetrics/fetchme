import mock

import inspect

from logme.config import read_config
from fetchme.utils import get_config_path, get_command_func, set_commands


def test_get_config_path(tmp_config):
    config_path = get_config_path()

    assert str(config_path) == f"{tmp_config}"


def test_get_command_func(tmp_config, mock_subprocess):
    config = read_config(tmp_config)
    subcommand = get_command_func('test_command', config)

    assert inspect.isfunction(subcommand)

    subcommand(None)

    mock_subprocess.assert_called_with(['ls', '-al'])


def test_set_commands(tmp_config):
    mock_group = mock.MagicMock()

    set_commands(mock_group)

    mock_group.command.assert_called_with(name='test_command')
    mock_group.command.return_value.assert_called()