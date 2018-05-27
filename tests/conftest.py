import pytest

import mock
import shutil
from pathlib import Path


@pytest.fixture
def tmp_config(mock_home_dir):
    project_dir = Path(__file__).parent.parent

    mock_config_path = mock_home_dir / '.fetchmerc'
    shutil.copyfile(project_dir / 'cfg/.fetchmerc', mock_config_path)

    with open(mock_config_path, 'a') as file:
        file.write("test_command=ls -al")

    yield mock_config_path


# ---------------------------------------------------------------------------
# mocks
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_home_dir(tmpdir, monkeypatch):
    monkeypatch.setattr('fetchme.utils.Path.home',
                        lambda: Path(tmpdir))

    yield Path(tmpdir)


@pytest.fixture
def mock_subprocess():
    with mock.patch('subprocess.call') as mock_:
        yield mock_
