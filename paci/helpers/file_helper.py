"""Helper to deal with downloads"""

import os
import shutil
import tarfile
import ruamel.yaml
from jinja2 import Template


def create_desktop_file(values, template):
    """Creates a .desktop file for Linux and replaces the template which actual values"""
    app_dir = os.path.join(os.environ.get("HOME"), ".local/share/applications")

    # Read the file
    with open(template, "r") as file:
        desktop_file_content = Template(file.read()).render(values)

    # Write the .desktop file
    desktop_file = os.path.join(app_dir, "{}.desktop".format(values["pkg_name"]))
    with open(desktop_file, "w") as file:
        file.write(desktop_file_content)

    # Make it executable
    os.chmod(desktop_file, 0o755)


def read_yaml(file):
    """Read a YAML file and return its contents as a dict."""
    if os.path.exists(file):
        with open(file, "r") as file:
            return ruamel.yaml.load(file.read(), ruamel.yaml.RoundTripLoader)
    else:
        file(file, "w").close()
        return False


def extract_tar_gz(working_dir, file):
    """Extract a .tar.gz archive."""
    if file.endswith("tar.gz"):
        tar = tarfile.open(file, "r:gz")
        tar.extractall(working_dir)
        tar.close()


def get_pkg_conf(pkg_recipe):
    """Read the RECIPE.yml and return it."""
    if pkg_recipe:
        # Read it
        conf = read_yaml(pkg_recipe)
        if not conf:
            print("Could not read RECIPE.yml.")
            exit(1)
        else:
            return conf
    else:
        print("Abort. RECIPE.yml could not be downloaded.")
        exit(1)
    return None


def safe_delete(file):
    """Safely deletes a given file"""
    if os.path.exists(file):
        os.remove(file)


def safe_copy(src, dest):
    """Safely copies a given file to the destination"""
    os.makedirs(dest, exist_ok=True)
    shutil.copy(src, dest)
