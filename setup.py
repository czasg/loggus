import os
import re
import codecs

from setuptools import setup, find_packages

"""pip install twine
1、python setup.py check
2、python setup.py sdist
3、twine upload dist/__packages__-__version__.tar.gz
"""

"""MANIFEST.in
global-include pat1 pat2 ... > Include all files anywhere
global-exclude pat1 pat2 ... > Exclude all files anywhere
graft dir-pattern > Include all files under directories matching dir-pattern
prune dir-pattern > Exclude all files under directories matching dir-pattern

such as: global-exclude *.py[cod]
"""


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r', encoding='utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='loggus',
    version=find_version('loggus', '__init__.py'),
    description="This is a log library, you can output json and care fields easy.",
    long_description="see https://github.com/CzaOrz/loggus",
    author='CzaOrz',
    author_email='972542644@qq.com',
    url='https://github.com/CzaOrz/loggus',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['loggus = loggus:execute', 'pyut = loggus:pyut']
    },
    install_requires=[
        "colorama",
        "coverage",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
