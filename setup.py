from pathlib import Path

from importlib.machinery import SourceFileLoader

from setuptools import setup, find_packages

ver_module_path = Path(__file__).parent / Path('fetchme/__version__.py')
ver_module_obj = SourceFileLoader('fetchme', str(ver_module_path)).load_module()

version = ver_module_obj.__version__

requires = [
    'click',
    'logme',
]


with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='fetchme',
    packages=find_packages(exclude=['tests*']),
    data_files=[
        (str(Path.home()), ['cfg/.fetchmerc']),
    ],
    install_requires=requires,
    version=version,
    description='package for caching and aliasing long commands',
    long_description=readme,
    author='Luna Chen',
    # url='https://github.com/BNMetrics/logme',
    author_email='luna@bnmetrics.com',
    keywords=['logging', 'cli'],
    python_requires='>=3',
    entry_points={'console_scripts': ['fetchme=fetchme:cli']},
    license='Apache 2.0',
)
