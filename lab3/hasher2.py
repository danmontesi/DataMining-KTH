import hashlib

import numpy as np

from hasher import Hasher


class Hasher2(Hasher):
    def __init__(self, mod):
        self.mod = mod

    def hash_value(self, value):
        a = hashlib.md5(str(value).encode('utf-8'))
        b = a.hexdigest()
        as_int = int(b, 16)
        with_mod = as_int%self.mod
        return with_mod

