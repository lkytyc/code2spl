from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load(self, file_path):
        self.image = Image.open(file_path)

    def save(self, file_path):
        if self.image is not None:
            self.image.save(file_path)

    def resize(self, dimensions):
        if self.image is not None:
            self.image = self.image.resize(dimensions)

    def rotate(self, degrees):
        if self.image is not None:
            self.image = self.image.rotate(degrees)

    def adjust_brightness(self, factor):
        if self.image is not None:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)

import unittest
import os

class ImageProcessorTestRotateImage(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.image_path = os.path.join(os.path.dirname(__file__), "test.png")
        image = Image.new("RGB", (100, 100), (255, 255, 255))
        image.save(self.image_path)

    def tearDown(self):
        self.processor.image.close()

    def test_rotate_image(self):
        self.processor.load_image(self.image_path)
        original_image = self.processor.image
        self.processor.rotate_image(90)
        self.assertTrue(ImageChops.difference(original_image.rotate(90), self.processor.image).getbbox() is None)

    def test_rotate_image_2(self):
        self.processor.load_image(self.image_path)
        original_image = self.processor.image
        self.processor.rotate_image(180)
        self.assertTrue(ImageChops.difference(original_image.rotate(180), self.processor.image).getbbox() is None)

    def test_rotate_image_3(self):
        self.processor.load_image(self.image_path)
        original_image = self.processor.image
        self.processor.rotate_image(270)
        self.assertTrue(ImageChops.difference(original_image.rotate(270), self.processor.image).getbbox() is None)

    def test_rotate_image_4(self):
        self.processor.load_image(self.image_path)
        original_image = self.processor.image
        self.processor.rotate_image(360)
        self.assertTrue(ImageChops.difference(original_image.rotate(360), self.processor.image).getbbox() is None)

    def test_rotate_image_5(self):
        self.processor.load_image(self.image_path)
        original_image = self.processor.image
        self.processor.rotate_image(45)
        self.assertTrue(ImageChops.difference(original_image.rotate(45), self.processor.image).getbbox() is None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
