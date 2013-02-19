# Copyright (c) 2011, Andres Moreira <andres@andresmoreira.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the authors nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ANDRES MOREIRA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import snappy
from unittest import TestCase

class SnappyCompressionTest(TestCase):
    def test_simple_compress(self):
        text = b"hello world!"
        compressed = snappy.compress(text)
        self.assertEquals(text, snappy.uncompress(compressed))

    def test_moredata_compress(self):
        text = b"snappy +" * 1000 + b" " + b"by " * 1000 + b" google"
        compressed = snappy.compress(text)
        self.assertEquals(text, snappy.uncompress(compressed))

    def test_randombytes_compress(self):
        _bytes = os.urandom(1000)
        compressed = snappy.compress(_bytes)
        self.assertEquals(_bytes, snappy.uncompress(compressed))

    def test_randombytes2_compress(self):
        _bytes = os.urandom(10000)
        compressed = snappy.compress(_bytes)
        self.assertEquals(_bytes, snappy.uncompress(compressed))

    def test_uncompress_error(self):
        self.assertRaises(snappy.UncompressError, snappy.uncompress, b"hoa")

    def test_unicode_compress(self):
        text = u"hello unicode world!"
        compressed = snappy.compress(text, encoding='utf-8')
        self.assertEquals(text, snappy.uncompress(compressed, decoding='utf-8'))

    def test_decompress(self):
        # decompress == uncompress, just to support compatibility with zlib
        text = b"hello world!"
        compressed = snappy.compress(text)
        self.assertEquals(text, snappy.decompress(compressed))

    def test_big_string(self):
        text = b'a'*10000000
        compressed = snappy.compress(text)
        self.assertEquals(text, snappy.decompress(compressed))


class SnappyValidBufferTest(TestCase):

    def test_valid_compressed_buffer(self):
        text = b"hello world!"
        compressed = snappy.compress(text)
        uncompressed = snappy.uncompress(compressed)
        self.assertEquals(text == uncompressed, snappy.isValidCompressed(compressed))

    def test_invalid_compressed_buffer(self):
        self.assertFalse(snappy.isValidCompressed(b"not compressed"))

if __name__ == "__main__":
    # in case nose is not installed
    import unittest
    unittest.main()
