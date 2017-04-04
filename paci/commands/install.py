"""The install command."""

import requests
import tempfile
import os
import ruamel.yaml
import hashlib
import shutil
import requests
from .base import Base
from clint.textui import progress
from jsontraverse.parser import JsonTraverseParser


class Install(Base):
    """Install!"""

    def __download(self, url, path, sha512sum=None, debug_mode=False):
        """Download a file, show the progress and do integrity checks."""

        file = url.split('/')[-1]
        file_path = path + "/" + file

        if self.__url_exists(url):
            print("Downloading " + file + "...")
            print("Directory: " + file_path)

            # Process the download and show progress
            if not debug_mode:
                req = requests.get(url, stream=True)
                with open(file_path, 'wb') as f:
                    total_length = int(req.headers.get('content-length'))
                    for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()

                # Verify that the download was successful
                if sha512sum is not None:
                    if not self.__verify_file(file_path, sha512sum):
                        print(file + " could not be downloaded.")
                        exit(1)

                print("Download: Successful \n")
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

    def run(self):
        PACI_TEMP = '/tmp/paci'
        registry_url = 'https://raw.githubusercontent.com/tradebyte/paci_packages/master'

        args = self.options
        pkg_files = {
            'GET.json': '',
            'INSTALL.sh': '',
            'DESKTOP': '',
            'CONF.tar.gz': '',
        }

        pkg_name = args['<package>']
        pkg_url = registry_url + "/" + pkg_name

        print("Package: " + pkg_name + "\n")

        # Handle arguments
        debug_mode = False if args['--debug'] is None else args['--debug']

        # Create temporary package directory
        os.makedirs(PACI_TEMP, exist_ok=True)
        pkg_temp_dir = tempfile.mkdtemp(dir=PACI_TEMP, prefix=pkg_name + '_')

        # Download RECIPE.yml
        pkg_recipe = self.__download(pkg_url + "/RECIPE.yml", pkg_temp_dir)
        if pkg_recipe:
            # Read it
            pkg_conf = self.__read_yaml(pkg_recipe)
            if not pkg_conf:
                print("Could not read RECIPE.yml.")
                exit(1)
        else:
            print("Abort. RECIPE.yml could not be downloaded.")
            exit(1)

        # Download all meta files
        for (file, path) in pkg_files.items():
            pkg_files[file] = self.__download(pkg_url + "/" + file, pkg_temp_dir)

        # Download SOURCES.tar.gz
        if 'sources' in pkg_conf:
            pkg_files['SOURCES.tar.gz'] = self.__download(
                pkg_url + "/" + pkg_conf['sources'],
                pkg_temp_dir,
                pkg_conf['sha512sum']
            )

        # TODO: Extract SOURCES.tar.gz

        # Process GET.json
        with open(pkg_files['GET.json'], 'r') as get_file:
            parser = JsonTraverseParser(get_file.read())
            files = parser.traverse("get")

            # work through all downloads
            for file in files:
                url = file['source'].replace('{{VERSION}}', pkg_conf['version'])
                sha512sum = file['sha512sum']
                self.__download(url, pkg_temp_dir, sha512sum, debug_mode)

        # TODO: Execute INSTALL.sh

        # TODO: Process DESKTOP file (template -> move)

        # TODO: Extract CONF.tar.gz

        # Cleanup if successful
        if not args['--no-cleanup']:
            shutil.rmtree(pkg_temp_dir)
