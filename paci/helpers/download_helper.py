"""Helper class to deal with downloads"""

import hashlib
import requests
import os
from clint.textui import progress
from jsontraverse.parser import JsonTraverseParser
from jinja2 import Template


def download(url, path, sha512sum=None, hidden=None):
    """Download a file, show the progress and do integrity checks."""
    file = url.split("/")[-1]
    file_path = os.path.join(path, file)

    if url_exists(url):
        # Process the download and show progress
        req = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            total_length = int(req.headers.get("content-length"))
            for chunk in progress.bar(
                    req.iter_content(chunk_size=1024),
                    expected_size=(total_length / 1024) + 1,
                    label="{}: ".format(file),
                    hide=hidden
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
        # Verify that the download was successful
        if sha512sum is not None:
            if not verify_file(file_path, sha512sum):
                print("{} could not be downloaded.".format(file))
                exit(1)

        return file_path
    else:
        return False


def download_get_files(file, pkg_src, constants):
    """Download all files from the GET.json."""
    with open(file, "r") as get_file:
        parser = JsonTraverseParser(get_file.read())
        files = parser.traverse("get")

        # work through all downloads
        for file in files:
            url = Template(file["source"]).render(constants)
            sha512sum = file["sha512sum"]
            download(url, pkg_src, sha512sum)


def url_exists(url):
    """Check if a given url exists."""
    codes = [200, 302]  # 200 OK, 302 Found
    return True if requests.head(url).status_code in codes else False


def verify_file(file, sha512sum):
    """"Returns if a file is corrupted or not."""

    # make a hash object
    h = hashlib.sha512()

    # open file for reading in binary mode
    with open(file, "rb") as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b"":
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest() == sha512sum

