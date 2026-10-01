from PIL import Image, ImageEnhance


class ImageProcessor:
    def __init__(self):
        self.image = None

    def adjust_brightness(self, factor: float):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)

    def load_image(self, image_path: str):
        self.image = Image.open(image_path)

    def resize_image(self, width: int, height: int):
        if self.image:
            self.image = self.image.resize((width, height))

    def rotate_image(self, degrees):
        if self.image:
            self.image = self.image.rotate(degrees)

    def save_image(self, save_path: str):
        if self.image:
            self.image.save(save_path)

import unittest
import os

class ImageProcessorTestResizeImage(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.image_path = os.path.join(os.path.dirname(__file__), "test.png")
        image = Image.new("RGB", (100, 100), (255, 255, 255))
        image.save(self.image_path)

    def tearDown(self):
        self.processor.image.close()

    def test_resize_image(self):
        self.processor.load_image(self.image_path)
        self.processor.resize_image(30, 15)
        self.assertEqual(self.processor.image.size, (30, 15))

    def test_resize_image_2(self):
        self.processor.load_image(self.image_path)
        self.processor.resize_image(30, 15)
        self.assertEqual(self.processor.image.mode, "RGB")

    def test_resize_image_3(self):
        self.processor.load_image(self.image_path)
        self.processor.resize_image(30, 15)
        self.assertEqual(self.processor.image.format, None)

    def test_resize_image_4(self):
        self.processor.load_image(self.image_path)
        self.processor.resize_image(40, 20)
        self.assertEqual(self.processor.image.mode, "RGB")

    def test_resize_image_5(self):
        self.processor.load_image(self.image_path)
        self.processor.resize_image(50, 25)
        self.assertEqual(self.processor.image.format, None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
