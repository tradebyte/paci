# -*- coding: utf-8 -*-
"""The install command."""

import tempfile
import os
import ruamel.yaml
import hashlib
import shutil
import requests
import subprocess
import tarfile
from jinja2 import Template
from .base import Base
from clint.textui import progress
from jsontraverse.parser import JsonTraverseParser
from paci.helpers.settings import Settings


class Install(Base):
    """Install!"""

    def __download(self, url, path, sha512sum=None):
        """Download a file, show the progress and do integrity checks."""

        file = url.split('/')[-1]
        file_path = path + "/" + file

        if self.__url_exists(url):
            # Process the download and show progress
            req = requests.get(url, stream=True)
            with open(file_path, 'wb') as f:
                total_length = int(req.headers.get('content-length'))
                for chunk in progress.bar(
                        req.iter_content(chunk_size=1024),
                        expected_size=(total_length / 1024) + 1,
                        label=file + ': '
                ):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            # Verify that the download was successful
            if sha512sum is not None:
                if not self.__verify_file(file_path, sha512sum):
                    print(file + " could not be downloaded.")
                    exit(1)

            return file_path
        else:
            return False

    @staticmethod
    def __read_yaml(file):
        """Read a YAML file and return its contents as a dict."""

        if os.path.exists(file):
            with open(file, 'r') as f:
                return ruamel.yaml.load(f.read(), ruamel.yaml.RoundTripLoader)
        else:
            file(file, 'w').close()
            return False

    @staticmethod
    def __url_exists(url):
        """Check if a given url exists."""

        codes = [200, 302]  # 200 OK, 302 Found
        return True if requests.head(url).status_code in codes else False

    @staticmethod
    def __verify_file(file, sha512sum):
        """"This function returns if a file is not corrupted."""

        # make a hash object
        h = hashlib.sha512()

        # open file for reading in binary mode
        with open(file, 'rb') as file:
            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)

        return h.hexdigest() == sha512sum

    def __get_additional_files(self, file, pkg_src, constants):
        with open(file, 'r') as get_file:
            parser = JsonTraverseParser(get_file.read())
            files = parser.traverse("get")

            # work through all downloads
            for file in files:
                url = Template(file['source']).render(constants)
                sha512sum = file['sha512sum']
                self.__download(url, pkg_src, sha512sum)

    def __get_pkg_conf(self, pkg_recipe):
        if pkg_recipe:
            # Read it
            conf = self.__read_yaml(pkg_recipe)
            if not conf:
                print("Could not read RECIPE.yml.")
                exit(1)
            else:
                return conf
        else:
            print("Abort. RECIPE.yml could not be downloaded.")
            exit(1)
        return None

    @staticmethod
    def __execute_shell_script(script, working_dir):
        with open(script, 'r') as f:
            try:
                res = subprocess.check_output(['bash', '-c', f.read()], cwd=working_dir)
                for line in res.splitlines():
                    print(line.decode("utf-8"))
            except subprocess.CalledProcessError as e:
                print(e.output)

    @staticmethod
    def __set_script_variables(pkg_constants):
        for key, value in pkg_constants.items():
            os.environ[key] = value

    @staticmethod
    def __create_desktop_file(desktop_file_dir, pkg_constants, desktop_file):
        with open(desktop_file, 'r') as file:
            desktop_file = Template(file.read()).render(pkg_constants)
        with open(desktop_file_dir + '/' + pkg_constants['pkg_name'] + '.desktop', 'w') as file:
            file.write(desktop_file)

    @staticmethod
    def __extract_tar_gz(working_dir, file):
        if file.endswith("tar.gz"):
            tar = tarfile.open(file, "r:gz")
            tar.extractall(working_dir)
            tar.close()

    def run(self):
        settings_helper = Settings()

        if settings_helper.settings_exist() is False:
            settings_helper.write_settings(settings_helper.defaults)

        settings = settings_helper.fetch_settings()

        os.makedirs(settings["paci"]["base"], exist_ok=True)

        args = self.options

        pkg_files = {
            'GET.json': '',
            'INSTALL.sh': '',
            'DESKTOP': '',
            'CONF.tar.gz': '',
        }

        pkg_name = args['<package>']
        pkg_url = settings["paci"]["registry"]["main"] + "/" + pkg_name  # TODO: handle fallback repo

        # Create temporary package directory
        os.makedirs(settings["paci"]["temp"], exist_ok=True)
        pkg_temp_dir = tempfile.mkdtemp(dir=settings["paci"]["temp"], prefix=pkg_name + '_')

        print("Package: " + pkg_name)
        print("Package working directory: " + pkg_temp_dir + "\n")

        # Download RECIPE.yml
        pkg_recipe = self.__download(pkg_url + "/RECIPE.yml", pkg_temp_dir)
        pkg_conf = self.__get_pkg_conf(pkg_recipe)

        # Download all meta files
        for (file, path) in pkg_files.items():
            pkg_files[file] = self.__download(pkg_url + "/" + file, pkg_temp_dir)

        # Create package directory
        pkg_dir = settings["paci"]["base"] + "/" + pkg_name + "_" + pkg_conf['version']
        os.makedirs(pkg_dir, exist_ok=True)

        # Create package constants (e.g. used for the templates)
        pkg_constants = {
            'pkg_src': pkg_temp_dir,
            'pkg_dir': pkg_dir,
            'pkg_ver': pkg_conf['version'],
            'pkg_desc': pkg_conf['summary'],
            'pkg_name': pkg_conf['name']
        }

        if 'sources' in pkg_conf:
            pkg_files['SOURCES.tar.gz'] = self.__download(
                pkg_url + "/" + pkg_conf['sources'],
                pkg_constants['pkg_src'],
                pkg_conf['sha512sum']
            )

        if pkg_files['SOURCES.tar.gz']:
            self.__extract_tar_gz(pkg_constants['pkg_src'] + '/SOURCES', pkg_files['SOURCES.tar.gz'])

        if pkg_files['GET.json']:
            self.__get_additional_files(pkg_files['GET.json'], pkg_constants['pkg_src'], pkg_constants)

        if pkg_files['INSTALL.sh']:
            self.__set_script_variables(pkg_constants)
            self.__execute_shell_script(pkg_files['INSTALL.sh'], pkg_constants['pkg_src'])

        if pkg_files['DESKTOP']:
            desktop_file_dir = os.environ.get('HOME') + '/.local/share/applications'
            self.__create_desktop_file(desktop_file_dir, pkg_constants, pkg_files['DESKTOP'])

        if pkg_files['CONF.tar.gz']:
            conf_dir = pkg_constants['pkg_src'] + '/CONF'
            self.__extract_tar_gz(conf_dir, pkg_files['CONF.tar.gz'])
            subprocess.check_output(
                ['bash', '-c', "rsync -rt --ignore-existing " + conf_dir + "/ " + os.environ.get('HOME')],
                cwd=pkg_constants['pkg_src']
            )

        # Cleanup if successful
        if not args['--no-cleanup']:
            shutil.rmtree(pkg_temp_dir)
