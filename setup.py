"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname
from setuptools import find_packages, setup

from paci import __version__

this_dir = abspath(dirname(__file__))

setup(
    name="paci",
    version=__version__,
    description="Your friendly, lightweight and flexible package manager.",
    long_description=open('DESCRIPTION.rst').read(),
    url="https://github.com/tradebyte/paci",
    download_url="https://github.com/tradebyte/paci/archive/{}.tar.gz".format(__version__),
    author="Niklas Heer",
    author_email="niklas.heer@tradebyte.com",
    license=open('LICENSE').read(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Software Distribution",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
    keywords=["cli", "package-manager", "install", "linux", "ubuntu", "bash"],
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=[
        "docopt",
        "better_exceptions",
        "ruamel.yaml",
        "json-traverse",
        "clint",
        "requests",
        "jinja2",
        "tinydb",
        "tabulate",
        "fuzzywuzzy",
        "python-Levenshtein"
    ],
    entry_points={
        "console_scripts": [
            "paci=paci.cli:main",
        ],
    }
)
