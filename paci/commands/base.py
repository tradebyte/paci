# -*- coding: utf-8 -*-
"""The base command."""

from paci.helpers.settings import Settings
from paci.helpers.pkg_index import PkgIndex


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        settings_helper = Settings()

        if settings_helper.settings_exist() is False:
            settings_helper.write_settings(settings_helper.defaults)

        self.settings = settings_helper.fetch_settings()
        self.index = PkgIndex(self.settings["paci"]["base"])

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
