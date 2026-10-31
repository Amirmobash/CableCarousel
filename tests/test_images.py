import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image

import kabelkarussell


class ImageLoadingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.overrides = self.root / "kabelkarussell_recolored"
        self.overrides.mkdir()
        self.app = SimpleNamespace(image_dir=self.overrides)
        self.file_patch = patch.object(kabelkarussell, "__file__", str(self.root / "kabelkarussell.py"))
        self.file_patch.start()
        self.addCleanup(self.file_patch.stop)

    def image(self, path, color):
        Image.new("RGB", (12, 12), color).save(path)

    def load(self, color):
        return kabelkarussell.KabelKarussellApp.load_image_file(self.app, color)

    def test_shipped_unicode_asset_is_found_without_override_directory_assets(self):
        self.image(self.root / "Grün.png", "green")
        result = self.load("Grün")
        self.assertEqual(result.size, (160, 160))
        self.assertEqual(result.mode, "RGBA")
        self.assertEqual(result.getpixel((0, 0)), (0, 128, 0, 255))

    def test_recolored_image_takes_precedence(self):
        self.image(self.root / "Rot.png", "red")
        self.image(self.overrides / "Rot.png", "blue")
        self.assertEqual(self.load("Rot").getpixel((0, 0)), (0, 0, 255, 255))

    def test_corrupt_override_uses_shipped_image(self):
        (self.overrides / "Rot.png").write_bytes(b"not a PNG")
        self.image(self.root / "Rot.png", "red")
        self.assertEqual(self.load("Rot").getpixel((0, 0)), (255, 0, 0, 255))

    def test_missing_image_preserves_generated_fallback(self):
        self.assertIsNone(self.load("unknown"))


if __name__ == "__main__":
    unittest.main()
