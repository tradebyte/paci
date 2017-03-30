"""The install command."""

import requests
from .base import Base
from clint.textui import progress
from jsontraverse.parser import JsonTraverseParser


class Install(Base):
    """Install!"""

    @staticmethod
    def __download(url, path):
        file = url.split('/')[-1]
        req = requests.get(url, stream=True)
        file_path = path + "/" + file
        print("Downloading " + file + " into " + file_path)
        with open(file_path, 'wb') as f:
            total_length = int(req.headers.get('content-length'))
            for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def run(self):
        print('Hello, world!')
        args = self.options
        # print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        if args['--no-config']:
            print("no-config!")

        print("Package: " + args['<package>'])

        json = """
        {
            "get": [
                {
                    "source": "https://download.jetbrains.com/webide/PhpStorm-{{VERSION}}.tar.gz",
                    "sha512sum": "38d9b49ab60c5e315c4891ec4f0c261028ba7e5012effc174a8e044ed4a6d4052fbde6913815c7dd97b4fcd08852a55b4819bda77a4a8ff476141216a3ef57ee"
                },
                {
                    "source": "https://d3nmt5vlzunoa1.cloudfront.net/phpstorm/files/2015/12/PhpStorm_400x400_Twitter_logo_white.png",
                    "sha512sum": "2c6b469befaf6d9316ac38e97240d5031a418a327b8a6593cb17bae6ef0932f310fec6656bb4574740699155d332fb81261bc55de6090e0cb34af79451bfce20"
                }
            ]
        }
        """

        version = "2017.1"

        parser = JsonTraverseParser(json)
        files = parser.traverse("get")

        for idx, file in enumerate(files):
            files[idx]['source'] = file['source'].replace('{{VERSION}}', version)

        print(files[0]['source'])
        self.__download(files[0]['source'], '/tmp')



