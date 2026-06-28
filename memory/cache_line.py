"""
Represents one cache line.
"""


class CacheLine:

    def __init__(self, line_size):

        self.valid = False

        self.dirty = False

        self.tag = None

        self.data = bytearray(line_size)

    def invalidate(self):

        self.valid = False

        self.dirty = False

        self.tag = None

    def __str__(self):

        return (
            f"Valid={self.valid} "
            f"Dirty={self.dirty} "
            f"Tag={self.tag}"
        )