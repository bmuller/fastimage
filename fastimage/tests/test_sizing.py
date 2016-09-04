import unittest

from fastimage.detect import get_size

from .utils import async_test


class SizingTest(unittest.TestCase):
    @async_test
    async def test_png(self):
        url = "http://dummyimage.com/301x402.png"
        width, height = await get_size(url)
        self.assertEqual(width, 301)
        self.assertEqual(height, 402)

    @async_test
    async def test_jpg(self):
        url = "http://dummyimage.com/301x402.jpg"
        width, height = await get_size(url)
        self.assertEqual(width, 301)
        self.assertEqual(height, 402)

    @async_test
    async def test_gif(self):
        url = "http://dummyimage.com/301x402.gif"
        width, height = await get_size(url)
        self.assertEqual(width, 301)
        self.assertEqual(height, 402)

    @async_test
    async def test_webp(self):
        url = "https://www.gstatic.com/webp/gallery3/1_webp_ll.webp"
        width, height = await get_size(url)
        self.assertEqual(width, 400)
        self.assertEqual(height, 301)

        url = "https://www.gstatic.com/webp/gallery3/1_webp_a.webp"
        width, height = await get_size(url)
        self.assertEqual(width, 400)
        self.assertEqual(height, 301)
