class ImageProcessor:
    def __init__(self):
        self.image = None

    def adjust_brightness(self, factor):
        image_present = bool(self.image)
        if image_present:
            enhancer = ImageEnhance.Brightness(self.image)
            adjusted_image = enhancer.enhance(factor)
            self.image = adjusted_image

    def load_image(self):
        loaded_image = Image.open(image_path)
        self.image = loaded_image

    def resize_image(self, width, height):
        _condition_result = bool(self.image)
        if _condition_result:
            self.image = self.image.resize((width, height))

    def rotate_image(degrees):
        image_exists = bool(self.image)
        if image_exists:
            self.image = self.image.rotate(degrees)

    def save_image(self):
        image_present = bool(self.image)
        if image_present:
            self.image.save(save_path)

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
