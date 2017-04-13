![paci](https://raw.github.com/tradebyte/paci/master/media/paci-logo.png "Your agents are standing by.Your friendly, lightweight and flexible package manager.")

-----

# paci

Your friendly, lightweight and flexible package manager.

It is a package manager with can be used to distribute your own packages.
It is meant to install all packages in userland.

It currently targets Ubuntu 16.04.

__This is a work in progress. Do not use yet!__

## Requirements

- python3
- python3-venv
- rsync

## Setup

```
$ make
```

## Usage

These are the planned commands.

```
   install   Installs a package.
   update    Updates a package.
   remove    Removes a package.
   list      Lists all installed packages.
   search    Searches for a package.
```


## Some snippets


- Install package: `$ pip install -e .[test]`
- Run tests: `$ python setup.py test`
- Activate virtualenv: `. env/bin/activate`
- Deactivate virtualenv: `deactivate`
- If you'd like to cut a new release of this CLI tool: `$ python setup.py sdist bdist_wheel`


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
