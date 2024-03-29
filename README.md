![paci](https://raw.github.com/tradebyte/paci/master/.github/images/paci-logo.png "Your agents are standing by.Your friendly, lightweight and flexible package manager.")

-----
[![PyPI version](https://badge.fury.io/py/paci.svg)](https://badge.fury.io/py/paci) [![GitHub issues](https://img.shields.io/github/issues/tradebyte/paci.svg)](https://github.com/tradebyte/paci/issues) [![GitHub license](https://img.shields.io/github/license/tradebyte/paci.svg)](https://github.com/tradebyte/paci/blob/master/LICENSE)


# paci

Your friendly, lightweight and flexible package manager.

It is a package manager which can be used to distribute your own packages.
It is meant to install all packages in your userland.

Please see [Limitations](#limitations)

## Installation

### Via script

```
bash <(curl -s https://raw.githubusercontent.com/tradebyte/paci/master/.github/bin/install.sh)
```

The script takes two parameter `main_registry` and `fallback_registry`. If you want to use them for your setup just append them accordingly.

Example:
```
bash <(curl -s https://raw.githubusercontent.com/tradebyte/paci/master/.github/bin/install.sh) https://raw.githubusercontent.com/tradebyte/paci/master
```
(which would define the main registry)

### Manually

On Ubuntu 16.04:

```bash
pip3 install paci
```

After that you should add `$HOME/.local/bin` to your `$PATH` in your `~/.bashrc` file.

```bash
export PATH="$PATH:$HOME/.local/bin"
```

## Requirements

- python3
- python3-venv
- rsync

## Setup

```
❯ make
```

## Usage

These are the planned commands.

```
❯ paci --help
paci

Usage:
  paci install [--no-config] [--no-cleanup] [--reuse] [--overwrite] [--debug] <package>...
  paci update [--no-config] [--no-cleanup] [--reuse] [--overwrite] [--debug] <package>...
  paci search <package>
  paci refresh
  paci list [--installed]
  paci remove
  paci configure [--no-choice] [--silent] [--main-registry=<url>] [--fallback-registry=<url>]
  paci generate (repo-index <path> | pkg-index)
  paci --help
  paci --version

Options:
  -h, --help                         Show this screen.
  -v, --version                      Show version.
  -n, --no-config                    Omits the config.
  -c, --no-cleanup                   Don't cleanup the mess.
  -o, --overwrite                    Overwrite the config.
  -d, --debug                        Print debugging messages.
  -i, --installed                    List all installed packages.
  -r, --reuse                        Reuse the downloaded files.
                                     (only possible with --no-cleanup)
  --no-choice                        Omit the questions and use the defaults.
  --silent                           Don't print anything.
  --main-registry=<url>              Set the <url> as default for the main registry.
  --fallback-registry=<url>          Set the <url> as default for the fallback registry.

Examples:
  paci install phpstorm

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tradebyte/paci

```

## Limitations

* It currently targets Ubuntu only!
* It needs more packages.
* It needs testing.
* It only supports 64bit systems.

## Some snippets

- Run tests: `$ python setup.py test`
- Activate virtualenv: `. env/bin/activate`
- Deactivate virtualenv: `deactivate`
- Run the linter: `pylint paci`
- New release of this CLI tool (pip): `$ python setup.py sdist bdist_wheel`

## Releasing a new version

### What you need to release a new paci version

- Make sure to install `wheel` and `twine` via pip.
- Have a [pypi-account](https://pypi.org/account/register/) with access to the paci package.

### Releasing

1. Bump up the version number in `paci/__init__.py` according to [semver](https://semver.org/).
2. Build: `python setup.py sdist bdist_wheel`
3. Test: `twine check dist/*`
4. Publish it to the test.pypi.org registry: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
5. Check if everything worked on the test.pypi.org site.
6. Publish it for real: `twine upload dist/*`

### Releasing to PyPI automatically

You can release a new version by using Github workflow automatically.

1. Bump up the version number in `paci/__init__.py` according to [semver](https://semver.org/).
2. Create a new release tag version and it will start our pipeline and push the new version to PyPI and PyPI test after it is merged to main.

## Contributing

See the [CONTRIBUTING] document.<br/>
Thank you, [contributors]!

  [CONTRIBUTING]: .github/CONTRIBUTING.md
  [contributors]: https://github.com/tradebyte/paci/graphs/contributors

## License

Copyright (c) 2017 by the Tradebyte Software GmbH.<br/>
`paci` is free software, and may be redistributed under the terms specified in the [LICENSE] file.

  [LICENSE]: /LICENSE

## About

`paci` is maintained and funded by the Tradebyte Software GmbH. <br/>
The names and logos for `paci` are trademarks of the Tradebyte Software GmbH.

We love free software!
