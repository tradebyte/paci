import sys
import time
import subprocess
import os
from halo import Halo
from log_symbols import LogSymbols
from termcolor import colored

from paci.packages.shell import Shell

DELAY = 0.1  # time to wait for I/O to finish
DEBUG = False or bool(os.environ.get("debug"))


def debug_execute(cmd, cwd=None):
    print("Executing command: " + cmd)
    popen = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True,
                             cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def sh(cmd, cwd=None):
    """Runs a command and returns it's output

    Parameters
    ----------
    cmd : str
        The shell command which will be executed.
    cwd : str, optional
        The path to the working directory.

    Returns
    -------
    False if the execution of the command failed.
    True if the execution was successful but no output was given.
    The output of the command if it was successful and stdout wasn't empty.
    """
    if DEBUG:
        stdout = ""
        for path in debug_execute(cmd, cwd=cwd):
            print(path, end="")
            stdout += path
        if stdout:
            return stdout.rstrip()
        else:
            return False
    else:
        executed_cmd = Shell(cmd, cwd=cwd)
        if executed_cmd.code == 0:
            if executed_cmd.stdout:
                return str(executed_cmd)
            else:
                return True
        else:
            return False


def without_keys(dictionary, keys):
    """Filters a dict and returns it. Everything in the keys list is filtered out.

    Parameters
    ----------
    dictionary : dict
        The dict which will be filtered.
    keys : list
        A list of keys as strings which will be filtered out of the dict.

    Returns
    -------
    A dict without the mentioned keys.
    """
    return {k: dictionary[k] for k in dictionary if k not in keys}


def abort_script(msg):
    """Aborts the script and outputs a message.

    Parameters
    ----------
    msg : str
        The message which will be displayed when exiting.
    """
    sys.exit("\n{} {}".format(symbol("err"), colored(msg, 'red', attrs=['bold'])))


def symbol(name):
    """Helper function to print symbols.

    Parameters
    ----------
    name : str
        You can choose a symbol by its name. These are the symbols:
           name    symbol
            []   -  ❐
            ?    -  ❓
            ok   -  ✔
            err  -  ✖
            warn -  ⚠
            info -  ℹ

    Returns
    -------
    A string containing the symbol as a Unicode char.
    """
    switcher = {
        "info": LogSymbols.INFO.value,
        "warn": LogSymbols.WARNING.value,
        "err": LogSymbols.ERROR.value,
        "ok": LogSymbols.SUCCESS.value,
        "?": colored('❓', 'red'),
        "[]": colored('❐', 'blue')
    }
    return switcher.get(name, "")


def print_heading(icon, text, color="yellow"):
    """Helper function to print a heading.

    Parameters
    ----------
    icon : str
        Describe a name of a symbol from the symbol() function.
    text : str
        The text of the heading.
    color : str, optional
        The color of the heading.
    """
    print("\n{} {}".format(symbol(icon), colored(text, color)))


def ask_with_default(question, default):
    """Helper function to get input from the use and if enter is pressed use the default.

    Parameters
    ----------
    question : str
        This is the question which will be displayed.
    default : str, optional
        You can set it to any string. It describes the default answer to the question.

    Returns
    -------
    Returns the answer to the question as a string.
    """
    return input("{} {} ({}): ".format(symbol("?"), question, default)) or default


def ask_yes_no(question, default="yes"):
    """Helper function to ask a yes/no question.

    Parameters
    ----------
    question : str
        This is the question which will be displayed.
    default : str, optional
        You can set it to "no". It describes the default answer to the question.

    Returns
    -------
    True if the answer is yes, else it returns False.
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input("\n{} {}{}".format(symbol("?"), question, prompt)).lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no'.\n")


def run_cmd(msg, cmd, ok_msg="", err_msg="", exit_msg="", exit_all=False, cwd=None):
    """Helper function to execute a command and use spinners.

    Parameters
    ----------
    msg : str
        You should describe what the command is doing in simple words.
    cmd : str, list
        The command you want to execute. Each parameter can be added to the list.
    ok_msg : str, optional
        The text you want to display if the command is executed successfully.
    err_msg : str, optional
        The text you want to display if the command fails.
    exit_msg : str, optional
        The additional information you want to display if the whole script is stopped.
    exit_all : bool, optional
        Whether you want to exit the complete script if the command fails.
    cwd : str, optional
        The path to the working directory.

    Returns
    -------
    True if the command was successful else it returns False.
    If there is an output and it was successful it returns the output of the command.
    """
    if DEBUG:
        print(colored(msg, "yellow"))
        return sh(cmd if type(cmd) is str else " ".join(cmd), cwd=cwd)
    else:
        spinner = Halo(text=msg, spinner='dots', color='blue')
        spinner.start()
        time.sleep(DELAY)  # If this is cut out some IO operations will fail
        stdout = sh(cmd if type(cmd) is str else " ".join(cmd), cwd=cwd)
        if stdout:
            spinner.succeed(colored(ok_msg if ok_msg else msg, 'green'))
            return stdout
        else:
            spinner.fail(colored(err_msg if err_msg else msg + " Failed!", "red"))
            if exit_all:
                abort_script("Aborting script! " + exit_msg)
        return False


def check_version(msg, name, desired_version, current_version):
    """Checks if a version is sufficient.

    Parameters
    ----------
    msg : str
        You should describe what it is doing in simple words.
    name: str
        The name of the software which is version checked
    desired_version : tuple
        The version number in tuple formatting. (e.g. (1, 5, 4))
    current_version : str
        The version to check. (e.g. 1.5.4)
    """
    spinner = Halo(text=msg, spinner='dots', color='blue')
    spinner.start()
    time.sleep(DELAY)  # If this is cut out some IO operations will fail
    version_as_ints = (int(x) for x in current_version.split('.'))
    if tuple(version_as_ints) >= desired_version:
        spinner.succeed(colored("Version of {} is sufficient!".format(name), "green"))
    else:
        ver = ".".join([str(num) for num in desired_version])
        spinner.fail(colored("{} requires version {}!".format(name, ver), "red"))
        abort_script("Aborting script! Please update {}!". format(name))
