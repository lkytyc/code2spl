from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None

    def adjust_brightness(self, factor: float):
        image_present = bool(self.image)
        if image_present:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)

    def load_image(self, image_path: str):
        self.image = Image.open(image_path)

    def resize_image(self, width: int, height: int):
        image_present = bool(self.image)
        if image_present:
            self.image = self.image.resize((width, height))

    def rotate_image(self, degrees):
        image_truthiness = bool(self.image)
        if image_truthiness:
            self.image = self.image.rotate(degrees)

    def save_image(self, save_path: str):
        has_image = bool(self.image)
        if has_image:
            save_result = self.image.save(save_path)

import unittest
import os

class ImageProcessorTestLoadImage(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.image_path = os.path.join(os.path.dirname(__file__), "test.png")
        image = Image.new("RGB", (100, 100), (255, 255, 255))
        image.save(self.image_path)

    def tearDown(self):
        self.processor.image.close()
        # if os.path.exists(self.image_path):
        #     os.remove(self.image_path)

    def test_load_image(self):
        self.processor.load_image(self.image_path)
        self.assertIsNotNone(self.processor.image)

    def test_load_image_2(self):
        self.processor.load_image(self.image_path)
        self.assertEqual(self.processor.image.size, (100, 100))

    def test_load_image_3(self):
        self.processor.load_image(self.image_path)
        self.assertEqual(self.processor.image.mode, "RGB")

    def test_load_image_4(self):
        self.processor.load_image(self.image_path)
        self.assertEqual(self.processor.image.format, "PNG")

    def test_load_image_5(self):
        self.processor.load_image(self.image_path)
        self.assertEqual(self.processor.image.filename, self.image_path)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
