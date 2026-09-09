"""Offline CLI contracts using the real OpenAI SDK and an in-process transport."""
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import openai
from openai import OpenAI

# SDK 3 moved its transport from httpx to httpx2; test both supported installs.
if int(openai.__version__.split('.')[0]) >= 3:
    import httpx2 as httpx
else:
    import httpx

from gpt_image_cli import cli

MODELS = ('gpt-image-2.5-flare', 'gpt-image-2.5-sunburst')
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')


def parse(*flags):
    with patch.object(sys, 'argv', ['gpt-image', '-p', 'Offline test', *flags]):
        return cli.parse_args()


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.image = self.folder / 'reference.png'
        self.image.write_bytes(PNG)
        self.requests = []
        self.response_status = 200
        self.client = OpenAI(api_key='offline-test-not-a-real-key', max_retries=0,
                             http_client=httpx.Client(transport=httpx.MockTransport(self.respond)))
        self.addCleanup(self.client.close)

    def respond(self, request):
        self.requests.append(request)
        body = {'created': 0, 'data': [{'b64_json': base64.b64encode(PNG).decode()}]}
        if self.response_status != 200:
            body = {'error': {'message': 'Test failure', 'type': 'invalid_request_error',
                              'code': 'insufficient_quota' if self.response_status == 429 else 'permission_denied'}}
        return httpx.Response(self.response_status, json=body, request=request)

    def test_default_preserved_and_models_not_rewritten(self):
        self.assertEqual(parse().model, 'gpt-image-2')
        for model in (*MODELS, *(m + '-2026-09-08' for m in MODELS), 'gpt-image-2'):
            with self.subTest(model=model):
                self.assertEqual(parse('--model', model).model, model)

    def test_quality_options(self):
        for model in MODELS:
            for quality in ('auto', 'low', 'medium', 'high', 'xhigh', 'max'):
                with self.subTest(model=model, quality=quality):
                    self.assertEqual(parse('--model', model, '--quality', quality).quality, quality)
        self.assertEqual(parse('--model', MODELS[0] + '-2026-09-08', '--quality', 'max').quality, 'max')

    def test_invalid_parameters_stop_before_request(self):
        cases = [('--quality', 'max'), ('--model', 'gpt-image-1.5', '--quality', 'xhigh'),
                 ('--model', MODELS[0] + '-typo', '--quality', 'max'),
                 ('--background', 'transparent', '--format', 'jpeg'), ('--n', '0'), ('--n', '11'),
                 ('--compression', '-1'), ('--compression', '101'),
                 ('--mask', str(self.image))]
        for flags in cases:
            with self.subTest(flags=flags), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    parse(*flags)
                self.assertEqual(raised.exception.code, 2)
        self.assertEqual(self.requests, [])

    def test_size_constraints(self):
        for model in (*MODELS, 'gpt-image-2'):
            for size in (*cli.SIZE_SHORTCUTS, 'auto', '1024x640', '3840x2160', '1536x512'):
                with self.subTest(model=model, size=size):
                    parse('--model', model, '--size', size)
            for size in ('0x1024', '1025x1024', '4096x1024', '1024x256', '256x256', '3840x3840', 'oops'):
                with self.subTest(model=model, size=size), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        parse('--model', model, '--size', size)

    def test_generate_serialization(self):
        for model in MODELS:
            for quality in ('high', 'xhigh', 'max'):
                with self.subTest(model=model, quality=quality):
                    args = parse('--model', model, '--quality', quality, '--background', 'transparent',
                                 '--format', 'webp', '--compression', '80', '--user', 'offline-user')
                    cli.call_generate(self.client, args)
                    request = self.requests[-1]
                    self.assertEqual(request.url.path, '/v1/images/generations')
                    body = json.loads(request.content)
                    self.assertEqual(body['model'], model)
                    self.assertEqual(body['quality'], quality)
                    self.assertEqual(body['background'], 'transparent')
                    self.assertEqual(body['output_format'], 'webp')
                    self.assertEqual(body['output_compression'], 80)
                    self.assertEqual(body['moderation'], cli.DEFAULT_MODERATION)
                    self.assertEqual(body['user'], 'offline-user')
                    self.assertNotIn('input_fidelity', body)
                    self.assertNotIn('response_format', body)

    def test_png_compression_omitted(self):
        args = parse('--model', MODELS[0], '--compression', '80')
        cli.call_generate(self.client, args)
        self.assertNotIn('output_compression', json.loads(self.requests[-1].content))
        args.image = [self.image]
        cli.call_edit(self.client, args)
        self.assertNotIn(b'name="output_compression"', self.requests[-1].content)

    def test_edit_and_multi_reference_mask_serialization(self):
        other = self.folder / 'second.png'
        other.write_bytes(PNG)
        mask = self.folder / 'mask.png'
        mask.write_bytes(PNG)
        for model in MODELS:
            for extra in ([], ['-i', str(other)], ['-m', str(mask)]):
                with self.subTest(model=model, extra=extra):
                    args = parse('--model', model, '-i', str(self.image), '--quality', 'max',
                                 '--background', 'transparent', '--format', 'png', *extra)
                    cli.call_edit(self.client, args)
                    request = self.requests[-1]
                    self.assertEqual(request.url.path, '/v1/images/edits')
                    body = request.content.decode('latin1')
                    self.assertIn(model, body)
                    self.assertIn('reference.png', body)
                    self.assertIn('max', body)
                    self.assertIn('transparent', body)
                    self.assertNotIn('name="input_fidelity"', body)
                    self.assertNotIn('name="moderation"', body)
                    if extra:
                        self.assertIn(Path(extra[1]).name, body)

    def test_fidelity_only_dropped_for_image2(self):
        for model, dropped in [('gpt-image-2', True), ('gpt-image-2-2026-04-21', True),
                               (MODELS[0], False), (MODELS[1], False), ('gpt-image-1.5', False)]:
            with self.subTest(model=model), contextlib.redirect_stderr(io.StringIO()):
                cli.call_edit(self.client, parse('--model', model, '-i', str(self.image), '--input-fidelity', 'high'))
                self.assertEqual(b'name="input_fidelity"' not in self.requests[-1].content, dropped)

    def test_missing_edit_file_no_request(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            cli.call_edit(self.client, parse('--model', MODELS[0], '-i', str(self.folder / 'missing.png')))
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(self.requests, [])

    def test_main_output_and_endpoint_routing(self):
        for flags, endpoint in [([], 'generations'), (['-i', str(self.image)], 'edits')]:
            path = self.folder / (endpoint + '.png')
            with patch.object(sys, 'argv', ['gpt-image', '-p', 'Offline test', '--model', MODELS[0], '-f', str(path), *flags]), \
                 patch.object(cli, '_load_env_chain'), patch.dict(os.environ, {'OPENAI_API_KEY': 'offline-test'}), \
                 patch.object(cli, 'OpenAI', return_value=self.client) as constructor, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(), 0)
                constructor.assert_called_once_with(max_retries=0)
            self.assertEqual(path.read_bytes(), PNG)
            self.assertEqual(self.requests[-1].url.path, '/v1/images/' + endpoint)

    def test_api_errors_no_fallback_or_output(self):
        for status in (403, 429):
            self.response_status = status
            self.requests.clear()
            path = self.folder / f'{status}.png'
            with patch.object(sys, 'argv', ['gpt-image', '-p', 'Offline test', '--model', MODELS[1], '-f', str(path)]), \
                 patch.object(cli, '_load_env_chain'), patch.dict(os.environ, {'OPENAI_API_KEY': 'offline-test'}), \
                 patch.object(cli, 'OpenAI', return_value=self.client), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cli.main(), 1)
            self.assertEqual(len(self.requests), 1)
            self.assertEqual(json.loads(self.requests[0].content)['model'], MODELS[1])
            self.assertFalse(path.exists())

    def test_missing_key_no_client(self):
        with patch.object(sys, 'argv', ['gpt-image', '-p', 'Offline test']), \
             patch.object(cli, '_load_env_chain'), patch.dict(os.environ, {}, clear=True), \
             patch.object(cli, 'OpenAI') as constructor, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(), 2)
            constructor.assert_not_called()

    def test_both_help_entrypoints(self):
        root = Path(__file__).resolve().parents[1]
        for script in ('src/gpt_image_cli/cli.py', 'skills/gpt-image/scripts/generate.py'):
            completed = subprocess.run([sys.executable, '-B', str(root / script), '--help'],
                                       cwd=self.folder, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('--model', completed.stdout)
            self.assertIn('xhigh', completed.stdout)


if __name__ == '__main__':
    unittest.main()
