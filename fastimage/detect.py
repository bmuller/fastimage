import asyncio
from io import BytesIO
import struct

import aiohttp
from aiohttp.errors import ClientOSError
from aiohttp import ClientResponseError

# Some help from:
# - http://bit.ly/1MYBDYv
# - https://github.com/philadams/dimensions
# - https://github.com/sdsykes/fastimage/blob/master/lib/fastimage.rb


class DownloadError(Exception):
    """
    Any issue downloading from the server (timeout, couldn't connect).
    """


class ImageCollector:
    def __init__(self, url):
        self.url = url
        self.size = None
        self.type = None

    async def collect(self):
        try:
            return await self._collect()
        except (ValueError, ClientOSError, asyncio.TimeoutError,
                ClientResponseError):
            msg = "Issue downloading first bytes of %s" % self.url
            raise DownloadError(msg)

    async def _collect(self):
        with aiohttp.Timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    await self._parse(response)

    async def _parse(self, response):
        body = bytes()
        # pylint: disable=not-callable
        chunk = await response.content.read(24)
        while chunk and len(body) < 3000000:
            body += chunk
            self.size, self.type = bytes_to_size(body)
            # we can terminate downloading once we get a size or know
            # that it's a type we can't get the size for easily
            if self.size is not None or self.type in ['bmp', 'tif']:
                response.close()
                return
            chunk = await response.content.read(8)


def gif(bites):
    try:
        return struct.unpack('<HH', bites[6:10])
    except struct.error:
        return None


def jpeg(bites):
    fhandle = BytesIO(bites)
    try:
        fhandle.seek(0)
        size = 2
        ftype = 0
        while not 0xc0 <= ftype <= 0xcf:
            fhandle.seek(size, 1)
            byte = fhandle.read(1)
            while ord(byte) == 0xff:
                byte = fhandle.read(1)
            ftype = ord(byte)
            size = struct.unpack('>H', fhandle.read(2))[0] - 2
        fhandle.seek(1, 1)
        height, width = struct.unpack('>HH', fhandle.read(4))
        return (width, height)
    except struct.error:
        return None
    except TypeError:
        return None


def webp(bites):
    # pylint: disable=invalid-name
    vp8 = bites[12:16]
    result = None
    if vp8 == b"VP8 " and len(bites) > 30:
        width, height = struct.unpack('<HH', bites[26:30])
        return [width & 0x3fff, height & 0x3fff]
    elif vp8 == b"VP8L" and len(bites) > 25:
        b1, b2, b3, b4 = bites[21:25]
        width = 1 + (((b2 & 0x3f) << 8) | b1)
        height = 1 + (((b4 & 0xF) << 10) | (b3 << 2) | ((b2 & 0xC0) >> 6))
        return [width, height]
    elif vp8 == b"VP8X" and len(bites) > 30:
        b1, b2, b3, b4, b5, b6 = struct.unpack('BBBBBB', bites[24:30])
        width = 1 + b1 + (b2 << 8) + (b3 << 16)
        height = 1 + b4 + (b5 << 8) + (b6 << 16)
        return [width, height]
    return result


def png(bites):
    try:
        check = struct.unpack('>i', bites[4:8])[0]
        if check != 0x0d0a1a0a:
            return None
        return struct.unpack('>ii', bites[16:24])
    except struct.error:
        return None


def bytes_to_size(bites):
    result = None, None
    if len(bites) < 24:
        return result

    peek = bites[0:2]
    if peek == b'GI':
        result = gif(bites), 'gif'
    elif peek == b'\xff\xd8':
        result = jpeg(bites), 'jpg'
    elif peek == b'\x89P':
        result = png(bites), 'png'
    elif peek == b"II" or peek == b"MM":
        result = None, 'tif'
    elif peek == b"BM":
        result = None, 'bmp'
    elif peek == b'RI' and bites[8:12] == b'WEBP':
        result = webp(bites), 'webp'
    return result


async def get_size(url):
    collector = ImageCollector(url)
    await collector.collect()
    return collector.size


async def get_type(url):
    collector = ImageCollector(url)
    await collector.collect()
    return collector.type
