"""
Cache statistics.
"""


class CacheStats:

    def __init__(self):

        self.read_hits = 0
        self.read_misses = 0

        self.write_hits = 0
        self.write_misses = 0

    @property
    def total_hits(self):

        return (
            self.read_hits +
            self.write_hits
        )

    @property
    def total_misses(self):

        return (
            self.read_misses +
            self.write_misses
        )

    @property
    def total_accesses(self):

        return (
            self.total_hits +
            self.total_misses
        )

    @property
    def hit_rate(self):

        if self.total_accesses == 0:
            return 0

        return (
            self.total_hits /
            self.total_accesses
        ) * 100

    def print(self):

        print()

        print("========== Cache ==========")

        print(
            f"Read Hits      : {self.read_hits}"
        )

        print(
            f"Read Misses    : {self.read_misses}"
        )

        print(
            f"Write Hits     : {self.write_hits}"
        )

        print(
            f"Write Misses   : {self.write_misses}"
        )

        print(
            f"Hit Rate       : {self.hit_rate:.2f}%"
        )

        print("===========================")