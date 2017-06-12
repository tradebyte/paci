![paci](https://raw.github.com/tradebyte/paci/master/media/paci-logo.png "Your agents are standing by.Your friendly, lightweight and flexible package manager.")

-----

# paci

Your friendly, lightweight and flexible package manager.

It is a package manager which can be used to distribute your own packages.
It is meant to install all packages in your userland.

Please see [Limitations](#limitations)

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
  paci install [--no-config] [--no-cleanup] [--reuse] [--overwrite] <package>...
  paci update [--no-config] [--no-cleanup] [--reuse] [--overwrite] <package>...
  paci search <package>
  paci refresh
  paci list
  paci remove
  paci configure
  paci generate (repo-index <path> | pkg-index)
  paci --help
  paci --version

Options:
  -h, --help                         Show this screen.
  -v, --version                      Show version.
  -n, --no-config                    Omits the config.
  -c, --no-cleanup                   Don't cleanup the mess.
  -o, --overwrite                    Overwrite the config.
  -r, --reuse                        Reuse the downloaded files.
                                     (only possible with --no-cleanup)

Examples:
  paci install phpstorm

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tradebyte/paci

```

## Limitations

* It currently targets Ubuntu 16.04 only!
* It needs more packages.
* It needs testing

## Some snippets

- Run tests: `$ python setup.py test`
- Activate virtualenv: `. env/bin/activate`
- Deactivate virtualenv: `deactivate`
- Run the linter: `pylint paci`
- New release of this CLI tool (pip): `$ python setup.py sdist bdist_wheel`


## Contributing

See the [CONTRIBUTING] document.<br/>
Thank you, [contributors]!

  [CONTRIBUTING]: CONTRIBUTING.md
  [contributors]: https://github.com/tradebyte/paci/graphs/contributors

## License

Copyright (c) 2017 by the Tradebyte Software GmbH.<br/>
`paci` is free software, and may be redistributed under the terms specified in the [LICENSE] file.

  [LICENSE]: /LICENSE

## About

`paci` is maintained and funded by the Tradebyte Software GmbH. <br/>
The names and logos for `paci` are trademarks of the Tradebyte Software GmbH.

We love free software!
