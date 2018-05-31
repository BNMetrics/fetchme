import mock

import inspect

from bnmutils import ConfigParser
from fetchme.utils import (_get_config_path, _get_command_func,
                           _set_commands, doc_parametrize)


def test_get_config_path(tmp_config):
    config_path = _get_config_path()

    assert str(config_path) == f"{tmp_config}"


def test_get_command_func(tmp_config, mock_subprocess):
    config = ConfigParser.from_files(tmp_config)
    subcommand = _get_command_func('test_command', config)

    assert inspect.isfunction(subcommand)

    subcommand(None)

    mock_subprocess.assert_called_with(['ls', '-al'])

    assert subcommand.__doc__.strip() == "Execute command alias 'test_command'; command: ls -al"


def test_set_commands(tmp_config):
    mock_group = mock.MagicMock()

    _set_commands(mock_group)

    mock_group.command.assert_called_with(name='test_command')
    mock_group.command.return_value.assert_called()


def test_doc_parametrize():
    @doc_parametrize(val1='hello', val2='world')
    def dummy_func():
        """
        This is my docstring, {val1}, {val2}
        """

    assert dummy_func.__doc__.strip() == 'This is my docstring, hello, world'
