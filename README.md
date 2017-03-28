# paci

Your friendly, lightweight and configurable package manager.

## Requirements

- python3
- python3-venv

## Setup

```
$ make
```


## Usage


If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is:

```
    $ pip install -e .[test]
```

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command:

```
    $ python setup.py test
```

This will trigger [py.test](http://pytest.org/latest/), along with its popular
[coverage](https://pypi.python.org/pypi/pytest-cov) plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index ([PyPI](https://pypi.python.org/pypi)), you can do so
by running:

```
    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*
```

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).


## Usage

```
[PCM] - (P)ackage & (C)onfiguration (M)anager

Usage:  pcm [global option] [command] [command option] [parameter]

PCM allows you to install software including their configuration.

[gloabl option]
  --version, -v                                                      Prints the version

[command]
  install, in [option: --no-config] [parameter: <package> <path>]    Installs the given <packages>.
                                                                     If given <path> is given it will install it their.
                                                                     If not it will install it in the deault location.
  update, up [option: --no-config] [parameter: <package>]            Updates the given <packages>.
  packages                                                           List available packages. (NYI)
  installed                                                          List installed packages. (NYI)
  remove, re [parameter: <package>]                                  Removes a installed <package>. (NYI)
  help                                                               Prints this help.

[command option]
  --no-config, -nc                                                   Omit the config files of a package from a command.

```



```
The most commonly used paci commands are:
   install   Installs a package.
   update    Updates a package.
   remove    Removes a package.
   list      Lists all installed packages.
   search    Searches for a package.
   
```
