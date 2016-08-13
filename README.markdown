# FastImage [![travis][travis-image]][travis-url]

[travis-image]: https://img.shields.io/travis/bmuller/fastimage/master.svg
[travis-url]: https://travis-ci.org/bmuller/fastimage


This is an implementation of the excellent Ruby library [FastImage](https://github.com/sdsykes/fastimage) - but for Python.

FastImage finds the size or type of an image given its uri by fetching as little as needed.

## Installation

```
pip install fastimage
```

## Usage

Usage is pretty dang simple.

```python
import asyncio
from fastimage.detect import get_size

loop = asyncio.get_event_loop()
url = "http://stephensykes.com/images/ss.com_x.gif"
width, height = loop.run_until_complete(get_size(url))
print("Size:", width, "x", height)
```

which will poop out:

```bash
Size: 266 x 56
```

You can also just get the image type:
```python
import asyncio
from fastimage.detect import get_type

loop = asyncio.get_event_loop()
url = "http://stephensykes.com/images/ss.com_x.gif"
result = loop.run_until_complete(get_type(url))
print("Type:", result)
```

which will poop out:

```bash
Type: gif
```

Right now, sizes can be deduced from gif / jpg / png.  Additionally, it can detect the type (but not size) of bmp / tiff.
