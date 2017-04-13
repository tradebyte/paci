"""Helper to deal with downloads"""

import os
import subprocess


def execute_shell_script(script, working_dir):
    """Execute a shell script."""
    with open(script, "r") as f:
        execute(f.read(), working_dir)


def set_script_variables(values):
    """Sets global variables which can be used by shell scripts."""
    for key, value in values.items():
        os.environ[key] = value


def rsync(wd, src, dest, ignore_existing=True):
    """rsync 2 folders"""
    if ignore_existing:
        cmd = "rsync -rt --ignore-existing {}/ {}".format(src, dest)
    else:
        cmd = "rsync -rt {}/ {}".format(src, dest)
    subprocess.check_output(["bash", "-c", cmd], cwd=wd)


def execute(commands, working_dir):
    """Executes a string containing bash commands."""
    try:
        res = subprocess.check_output(["bash", "-c", commands], cwd=working_dir)
        for line in res.splitlines():
            print(line.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(e.output)
