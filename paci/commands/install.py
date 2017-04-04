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

    @staticmethod
    def __download(url, path, debug_mode=False):

        file = url.split('/')[-1]
        file_path = path + "/" + file

        print("Downloading " + file + "...")
        print("Directory: " + file_path)

        if not debug_mode:
            req = requests.get(url, stream=True)
            with open(file_path, 'wb') as f:
                total_length = int(req.headers.get('content-length'))
                for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()

        return file_path

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

        args = self.options
        pkg_name = args['<package>']
        debug_mode = False if args['--debug'] is None else args['--debug']

        # print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        # if args['--no-config']:
        #     print("no-config!")

        print("Package: " + pkg_name + "\n")

        # Create temporary package directory
        os.makedirs(PACI_TEMP, exist_ok=True)
        pkg_temp_dir = tempfile.mkdtemp(dir=PACI_TEMP, prefix=pkg_name + '_')

        registry_url = 'https://raw.githubusercontent.com/tradebyte/paci_packages/master'
        pkg_url = registry_url + "/" + pkg_name

        # Download RECIPE.yml
        pkg_recipe = self.__download(pkg_url + "/RECIPE.yml", pkg_temp_dir)
        print("Download: Successful \n")

        # Read RECIPE.yml
        print("Reading RECIPE.yml...")
        with open(pkg_recipe, 'r') as recipe_file:
            pkg_conf = ruamel.yaml.load(recipe_file.read(), ruamel.yaml.RoundTripLoader)
            if debug_mode:
                print("name: " + pkg_conf['name'])
                print("version: " + pkg_conf['version'])
                print("summary: " + pkg_conf['summary'])
            print()

        # Download GET.json
        pkg_get = self.__download(pkg_url + "/GET.json", pkg_temp_dir)
        print("Download: Successful \n")

        # Process GET.json
        print("Processing GET.json... \n")
        with open(pkg_get, 'r') as get_file:
            parser = JsonTraverseParser(get_file.read())
            files = parser.traverse("get")

            # work through all downloads
            for file in files:
                url = file['source'].replace('{{VERSION}}', pkg_conf['version'])
                sha512sum = file['sha512sum']
                if self.__verify_file(self.__download(url, pkg_temp_dir, debug_mode), sha512sum, debug_mode):
                    print("Download: Successful \n")
                else:
                    print("Download: FAILED")
                    break

        # Cleanup if successful
        if not args['--no-cleanup']:
            shutil.rmtree(pkg_temp_dir)
