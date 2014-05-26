# Some help from http://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib
# and https://github.com/philadams/dimensions and https://github.com/sdsykes/fastimage/blob/master/lib/fastimage.rb
from StringIO import StringIO
import struct


def gif(bytes):
    try:
        return struct.unpack('<HH', bytes[6:10])
    except:
        return None


def jpeg(bytes):
    fhandle = StringIO(bytes)
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
        h, w = struct.unpack('>HH', fhandle.read(4))
        return w, h
    except:
        return None


def png(bytes):
    try:
        check = struct.unpack('>i', bytes[4:8])[0]
        if check != 0x0d0a1a0a:
            return None
        return struct.unpack('>ii', bytes[16:24])
    except:
        return None


def bytes_to_size(bytes):
    if len(bytes) < 24:
        return None

    peek = bytes[0:2]
    if peek == "GI":
        return gif(bytes), 'gif'
    elif peek == '\xff\xd8':
        return jpeg(bytes), 'jpg'
    elif peek == '\x89P':
        return png(bytes), 'png'
    elif peek == "II" or peek == "MM":
        return None, 'tif'
    if peek == "BM":
        return None, 'bmp'
    else:
        return None, None
