"""Tests for the settings helper."""

import unittest
import os
from unittest.mock import patch, mock_open
from paci.helpers.settings import Settings

settings_data_defaults = """paci:
    temp: /tmp/paci
    base: ~/.paci
    registry:
        main: https://raw.githubusercontent.com/tradebyte/paci_packages/master
        fallback: https://raw.githubusercontent.com/tradebyte/paci_packages/master
"""

settings_data_empty = """"""

settings_data_changed = """paci:
    temp: /tmp/temp
    base: /tmp/base
    registry:
        main: https://custom.main.url
        fallback: https://custom.fallback.url
"""

settings_data_changed_partial = """paci:
    base: /tmp/base
    registry:
        fallback: https://custom.fallback.url
"""


class TestSettingsHelper(unittest.TestCase):

    @patch("paci.helpers.settings.open", mock_open(read_data=settings_data_defaults))
    def test_fetch_settings_file_defaults(self):
        """Fetching a file with default values should break nothing"""
        helper = Settings()
        settings = helper.fetch_settings()
        expected = {
            "paci": {
                "temp": "/tmp/paci",
                "base": "~/.paci",
                "registry": {
                    "main": "https://raw.githubusercontent.com/tradebyte/paci_packages/master",
                    "fallback": "https://raw.githubusercontent.com/tradebyte/paci_packages/master"
                }
            }
        }
        self.assertDictEqual(expected, settings)

    @patch("paci.helpers.settings.open", mock_open(read_data=settings_data_empty))
    def test_fetch_settings_file_empty(self):
        """Fetching an empty file should break nothing"""
        helper = Settings()
        settings = helper.fetch_settings()
        expected = {
            "paci": {
                "temp": "/tmp/paci",
                "base": os.environ.get('HOME') + '/.paci',
                "registry": {
                    "main": "https://raw.githubusercontent.com/tradebyte/paci_packages/master",
                    "fallback": "https://raw.githubusercontent.com/tradebyte/paci_packages/master"
                }
            }
        }
        self.assertDictEqual(expected, settings)

    @patch("paci.helpers.settings.open", mock_open(read_data=settings_data_changed))
    def test_fetch_settings_file_changed(self):
        """Fetching a file with all values changed should result in settings without a default value"""
        helper = Settings()
        settings = helper.fetch_settings()
        expected = {
            "paci": {
                "temp": "/tmp/temp",
                "base": "/tmp/base",
                "registry": {
                    "main": "https://custom.main.url",
                    "fallback": "https://custom.fallback.url"
                }
            }
        }
        self.assertDictEqual(expected, settings)

    @patch("paci.helpers.settings.open", mock_open(read_data=settings_data_changed_partial))
    def test_fetch_settings_file_partial(self):
        """Fetching a file with partial values changed should result in settings without some default values"""
        helper = Settings()
        settings = helper.fetch_settings()
        expected = {
            "paci": {
                "temp": "/tmp/paci",
                "base": "/tmp/base",
                "registry": {
                    "main": "https://raw.githubusercontent.com/tradebyte/paci_packages/master",
                    "fallback": "https://custom.fallback.url"
                }
            }
        }
        self.assertDictEqual(expected, settings)

    def test_fetch_settings_use_standard_path(self):
        """Check if fetch_settings uses the standard path if none is given"""
        helper = Settings()

        with patch("paci.helpers.settings.open", mock_open(read_data=settings_data_defaults)) as m:
            helper.fetch_settings()

        expected_setting_path = os.environ.get('HOME') + '/.config/paci/settings.yml'
        m.assert_called_once_with(expected_setting_path, 'r')

    def test_write_settings(self):
        """Check if we call making dirs and the file handle for writing settings"""
        towrite = {
            "paci": {
                "temp": "/custom/temp",
                "base": "/custom/base",
                "registry": {
                    "main": "https://custom.main.url",
                    "fallback": "https://custom.fallback.url"
                }
            }
        }
        helper = Settings()

        with patch("os.makedirs", return_value=False) as m_os:
            with patch("paci.helpers.settings.open", mock_open(read_data=settings_data_defaults)) as m:
                helper.write_settings(data=towrite)

        expected_setting_path = os.environ.get('HOME') + '/.config/paci/settings.yml'
        expected_setting_dir_path = os.environ.get('HOME') + '/.config/paci'
        m_os.assert_called_once_with(expected_setting_dir_path, exist_ok=True)
        m.assert_called_once_with(expected_setting_path, 'w')

    def test_settings_exist(self):
        """Check if we return false if no setting file is there, yet"""
        helper = Settings()

        with patch("os.path.isfile", return_value=False) as m:
            self.assertFalse(helper.settings_exist())
