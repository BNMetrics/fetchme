from pathlib import Path

from importlib.machinery import SourceFileLoader

from setuptools import setup, find_packages
from setuptools.command.install import install


ver_module_path = Path(__file__).parent / Path('fetchme/__version__.py')
ver_module_obj = SourceFileLoader('fetchme', str(ver_module_path)).load_module()

version = ver_module_obj.__version__

home_dir = Path.home()

requires = [
    'click',
    'bnmutils'
]

data_files = [
        (str(home_dir), ['cfg/.fetchmerc']),
]


with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()


def post_install_cmd():
    """
    Post installation script for editing bash configuration file
    and allow command auto completion! :)

    * auto completion will only work on unix based systems *
    """
    import sys
    import re

    if re.sub('[^a-zA-Z]+', '', sys.platform.lower()) not in ['darwin', 'linux']:
        return

    bash_config_options = ['.bashrc', '.profile', '.bash_profile']

    for i in bash_config_options:
        if (home_dir / i).exists():
            bash_config = (home_dir / i)
            try:
                config_line = 'eval "$(_FETCHME_COMPLETE=source fetchme)"'
                content = bash_config.read_text()

                with bash_config.open('a') as file:
                    if config_line not in content:
                        file.write(f"{config_line}\n")
                break
            except PermissionError:
                pass


class PostInstall(install):
    """
    Post install commands to enable auto completion
    """
    def run(self):
        print('install ran')
        install.run(self)
        post_install_cmd()


setup(
    name='fetchme',
    packages=find_packages(exclude=['tests*']),
    data_files=data_files,
    cmdclass={
        'install': PostInstall,
    },
    install_requires=requires,
    version=version,
    description='package for caching and aliasing long commands',
    long_description=readme,
    author='Luna Chen',
    url='https://github.com/BNMetrics/fetchme',
    author_email='luna@bnmetrics.com',
    keywords=['alias', 'cli', 'command-aliasing', 'bash-aliasing'],
    python_requires='>=3',
    entry_points={'console_scripts': ['fetchme=fetchme:cli']},
    license='Apache 2.0',
)
