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

class ImageProcessorTestSaveImage(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.image_path = os.path.join(os.path.dirname(__file__), "test.png")
        image = Image.new("RGB", (100, 100), (255, 255, 255))
        image.save(self.image_path)

    def tearDown(self):
        self.processor.image.close()

    def test_save_image(self):
        save_path = os.path.join(os.path.dirname(__file__), "test_save.png")
        self.processor.load_image(self.image_path)
        self.processor.save_image(save_path)
        saved_image = Image.open(save_path)
        self.assertIsNotNone(saved_image)

    def test_save_image_2(self):
        save_path = os.path.join(os.path.dirname(__file__), "test_save.png")
        self.processor.load_image(self.image_path)
        self.processor.save_image(save_path)
        saved_image = Image.open(save_path)
        self.assertEqual(saved_image.size, (100, 100))

    def test_save_image_3(self):
        save_path = os.path.join(os.path.dirname(__file__), "test_save.png")
        self.processor.load_image(self.image_path)
        self.processor.save_image(save_path)
        saved_image = Image.open(save_path)
        self.assertEqual(saved_image.mode, "RGB")

    def test_save_image_4(self):
        save_path = os.path.join(os.path.dirname(__file__), "test_save.png")
        self.processor.load_image(self.image_path)
        self.processor.save_image(save_path)
        saved_image = Image.open(save_path)
        self.assertEqual(saved_image.format, "PNG")

    def test_save_image_5(self):
        save_path = os.path.join(os.path.dirname(__file__), "test_save.png")
        self.processor.load_image(self.image_path)
        self.processor.save_image(save_path)
        saved_image = Image.open(save_path)
        self.assertEqual(saved_image.filename, save_path)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
