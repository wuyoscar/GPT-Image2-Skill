"""Offline credential precedence with temporary files and fake keys only."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openai import OpenAI

from gpt_image_cli import cli


class CredentialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cwd = Path(self.tmp.name) / 'cwd'
        self.home = Path(self.tmp.name) / 'home'
        self.cwd.mkdir()
        self.home.mkdir()
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.enterContext(patch.object(cli.Path, 'cwd', return_value=self.cwd))
        self.enterContext(patch.object(cli.Path, 'home', return_value=self.home))

    def write_key(self, folder, value):
        (folder / '.env').write_text(f'OPENAI_API_KEY={value}\n', encoding='utf-8')

    def assert_selected_key(self, expected):
        cli._load_env_chain()
        self.assertEqual(os.environ.get('OPENAI_API_KEY'), expected)
        if expected:
            # Construction reads the selected environment value; no HTTP is sent.
            with OpenAI(max_retries=0) as client:
                self.assertEqual(client.api_key, expected)
                self.assertEqual(client.max_retries, 0)

    def test_process_key_wins(self):
        os.environ['OPENAI_API_KEY'] = 'fake-process-key'
        self.write_key(self.cwd, 'fake-cwd-key')
        self.write_key(self.home, 'fake-home-key')

        self.assert_selected_key('fake-process-key')

    def test_cwd_key_wins_over_home(self):
        self.write_key(self.cwd, 'fake-cwd-key')
        self.write_key(self.home, 'fake-home-key')

        self.assert_selected_key('fake-cwd-key')

    def test_home_key_fallback(self):
        (self.cwd / '.env').write_text('OTHER_SETTING=fake\n', encoding='utf-8')
        self.write_key(self.home, 'fake-home-key')

        self.assert_selected_key('fake-home-key')

    def test_no_key_stays_absent(self):
        self.assert_selected_key(None)
        self.assertNotIn('OPENAI_API_KEY', os.environ)

    def test_existing_empty_key_does_not_fall_back(self):
        os.environ['OPENAI_API_KEY'] = ''
        self.write_key(self.cwd, 'fake-cwd-key')
        self.write_key(self.home, 'fake-home-key')

        self.assert_selected_key('')
        self.assertIn('OPENAI_API_KEY', os.environ)


if __name__ == '__main__':
    unittest.main()
