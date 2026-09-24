class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, image_path):
        loaded_image = Image.open(image_path)
        self.image = loaded_image

    def save_image(self, save_path):
        if self.image:
            self.image.save(save_path)

    def resize_image(self, width, height):
        if self.image:
            self.image = self.image.resize((width, height))

    def rotate_image(self, degrees):
        if self.image:
            self.image = self.image.rotate(degrees)

    def adjust_brightness(self, factor):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            adjusted_image = enhancer.enhance(factor)
            self.image = adjusted_image

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
