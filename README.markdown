# FastImage

This is an implementation of the excellent Ruby library [FastImage](https://github.com/sdsykes/fastimage) - but for [Python Twisted](http://twistedmatrix.com).

FastImage finds the size or type of an image given its uri by fetching as little as needed.

## Installation

```
pip install fastimage
```

## Usage
*This assumes you have a working familiarity with [Twisted](http://twistedmatrix.com).*

Usage is pretty dang simple.

```python
from fastimage import get_size
from twisted.internet import reactor

def handle(result):
    width, height = result
    print "Size: ", width, "x", height
    reactor.stop()

url = "http://stephensykes.com/images/ss.com_x.gif"
get_size(url).addCallbacks(handle)
reactor.run()
```

which will poop out:

```bash
Size:  266 x 56
```

You can also just get the image type:
```python
from fastimage import get_type
from twisted.internet import reactor

def handle(result):
    print "Type:", result
    reactor.stop()

url = "http://stephensykes.com/images/ss.com_x.gif"
get_type(url).addCallbacks(handle)
reactor.run()
```

which will poop out:

```bash
Type: gif
```

Right now, sizes can be deduced from gif / jpg / png.  Additionally, it can detect the type (but not size) of bmp / tiff.
