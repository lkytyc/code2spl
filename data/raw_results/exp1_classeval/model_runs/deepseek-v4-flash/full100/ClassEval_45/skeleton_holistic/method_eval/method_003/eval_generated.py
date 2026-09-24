from PIL import Image, ImageEnhance

class ImageProcessor:
    """
    This is a class to process image, including loading, saving, resizing, rotating, and adjusting the brightness of images.
    """

    def __init__(self):
        """
        Initialize self.image
        """
        self.image = None

    def load_image(self, image_path):
        """
        Use Image util in PIL to open a image
        :param image_path: str, path of image that is to be
        """
        self.image = Image.open(image_path)

    def save_image(self, save_path):
        """
        Save image to a path if image has opened
        :param save_path: str, the path that the image will be saved
        """
        if self.image is not None:
            self.image.save(save_path)

    def resize_image(self, width, height):
        """
        Risize the image if image has opened.
        :param width: int, the target width of image
        :param height: int, the target height of image
        """
        if self.image is not None:
            self.image = self.image.resize((width, height))

    def rotate_image(self, degrees):
        """
        rotate image if image has opened
        :param degrees: float, the degrees that the image will be rotated
        """
        if self.image is not None:
            self.image = self.image.rotate(degrees)

    def adjust_brightness(self, factor):
        """
        Adjust the brightness of image if image has opened.
        :param factor: float, brightness of an image. A factor of 0.0 gives a black image. A factor of 1.0 gives the original image.
        """
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
