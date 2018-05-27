import pytest

from click.testing import CliRunner

from fetchme._cli import cli
from logme.config import read_config


class TestCli:

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

    # ---------------------------------------------------------------------------
    # 'fetchme edit' command test
    # ---------------------------------------------------------------------------

    def test_edit_command(self, mock_subprocess, tmp_config):
        result = self.runner.invoke(cli, ['edit'])

        mock_subprocess.assert_called_with(['vim', str(tmp_config)])
        assert result.exit_code == 0

    def test_edit_raise(self, mock_home_dir):
        with pytest.raises(FileNotFoundError) as e_info:
            result = self.runner.invoke(cli, ['edit'])
            assert result.exit_code == -1
            raise result.exception

        assert e_info.value.args[0] == f"{mock_home_dir / '.fetchmerc'} does not exist," \
                                       f" please reinstall or upgrade the package."

    # ---------------------------------------------------------------------------
    # 'fetchme set' test
    # ---------------------------------------------------------------------------
    def test_set(self, tmp_config):
        result = self.runner.invoke(cli, ['set', 'blah=hello'])

        config = read_config(tmp_config)

        assert result.exit_code == 0
        assert config.has_option('fetchme', 'blah')
        assert config.get('fetchme', 'blah') == 'hello'

    def test_set_override_existing(self, tmp_config):
        self.runner.invoke(cli, ['set', 'blah=hello'])
        result = self.runner.invoke(cli, ["set", 'blah=overriden value', '-o'])

        config = read_config(tmp_config)

        assert result.exit_code == 0
        assert config.get('fetchme', 'blah') == 'overriden value'

    def test_set_raise_already_exist(self, tmp_config):
        self.runner.invoke(cli, ["set", "test='blah'"])

        with pytest.raises(ValueError) as e_info:
            result = self.runner.invoke(cli, ["set", "test='blah'"])

            assert result.exit_code == -1
            raise result.exception

        assert e_info.value.args[0] == "'test' already exist! use --override, or -o flag to override"

    def test_set_raise_default_command(self, tmp_config):
        with pytest.raises(ValueError) as e_info:
            result = self.runner.invoke(cli, ['set', 'edit=edit my file'])
            raise result.exception

        assert result.exit_code == -1
        assert e_info.value.args[0] == "'edit' is a default command, and it cannot be set!"

    # ---------------------------------------------------------------------------
    # 'fetchme remove' test
    # ---------------------------------------------------------------------------
    def test_remove(self, tmp_config):
        self.runner.invoke(cli, ['set', 'to_remove="command to be removed"'])

        config = read_config(tmp_config)
        assert 'to_remove' in config.options('fetchme')

        self.runner.invoke(cli, ['remove', 'to_remove'])

        config_removed = read_config(tmp_config)
        assert 'to_remove' not in config_removed.options('fetchme')
