from twisted.web.http import PotentialDataLoss
import treq
from fastimage.detect import bytes_to_size


class ImageCollector:
    def __init__(self):
        self.body = ""
        self.size = None
        self.type = None

    def start(self, resp):
        self.resp = resp
        return treq.collect(resp, self.collect)

    def collect(self, data):
        self.body += data
        self.size, self.type = bytes_to_size(self.body)
        if self.size is not None:
            self.resp.cancel()
        if len(self.body) > 300000:
            raise PotentialDataLoss
