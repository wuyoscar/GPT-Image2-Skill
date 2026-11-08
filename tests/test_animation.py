"""Local animation contracts: cell order, timing, alpha, and safe output handling."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from gpt_image_cli.animation import grid_boxes, playback_order, main

class AnimationTests(unittest.TestCase):
    def test_grid_order_with_spacing(self):
        self.assertEqual(grid_boxes((9,9),2,2,1,1),[(1,1,4,4),(5,1,8,4),(1,5,4,8),(5,5,8,8)])
        with self.assertRaises(ValueError):grid_boxes((10,9),2,2,1,1)
        self.assertEqual(playback_order(4,True),[0,1,2,3,2,1])

    def test_gif_frames_timing_alpha_and_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);sheet=root/'sheet.png';out=root/'loop.gif';preview=root/'preview.html'
            im=Image.new('RGBA',(32,16))
            im.paste((255,0,0,255),(2,2,10,10));im.paste((0,255,0,255),(18,2,26,10));im.save(sheet)
            flags=['--sheet',str(sheet),'--columns','2','--rows','1','--duration','120','-f',str(out),'--preview',str(preview),'--title','<script>oops</script>']
            with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(main(flags),0)
            with Image.open(out) as gif:
                self.assertEqual(gif.n_frames,2);self.assertEqual(gif.info['loop'],0)
                self.assertEqual(gif.info['duration'],120);self.assertEqual(gif.size,(16,16))
                self.assertEqual(gif.convert('RGBA').getpixel((0,0))[3],0)
                self.assertEqual(gif.convert('RGB').getpixel((4,4)),(255,0,0))
                gif.seek(1);self.assertEqual(gif.convert('RGB').getpixel((4,4)),(0,255,0))
            body=preview.read_text();self.assertIn('&lt;script&gt;oops&lt;/script&gt;',body)
            self.assertNotIn('<script>oops</script>',body);self.assertIn('data:image/png;base64,',body)
            original=out.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):main(flags)
            self.assertEqual(out.read_bytes(),original)

    def test_source_and_preview_collision(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);sheet=root/'sheet.gif';Image.new('RGB',(32,16),'red').save(sheet)
            flags=['--sheet',str(sheet),'--columns','2','--rows','1','-f',str(sheet),'--force']
            original=sheet.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):main(flags)
            self.assertEqual(sheet.read_bytes(),original)
