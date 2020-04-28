import unittest

from models import Cache


class TestCache(unittest.TestCase):

    def test_default(self):
        cache = Cache(4)
        cache.add(1)
        cache.add('q')
        cache.add(0.99)
        cache.add('q')
        cache.add(0.988)

        self.assertEqual(cache.length, 4)

        cache.remove('q')
        self.assertEqual(cache.length, 2)

        cache = Cache(3)
        cache.add(1)
        cache.add('q')
        cache.add('a')
        cache.add('b')
        cache.add('c')
        self.assertEqual(cache.length, 3)

        values = cache.cache
        self.assertEqual(values[0], 'a')
        self.assertEqual(values[1], 'b')
        self.assertEqual(values[2], 'c')

        self.assertFalse(cache.exists(2))
        self.assertTrue(cache.exists('c'))

    def test_size_zero_and_less(self):
        cache = Cache(0)
        cache.add(2)
        cache.add(3)
        cache.add(4)
        cache.add(5)
        self.assertFalse(cache.exists(2))

        cache = Cache(-8)
        cache.add(2)
        cache.add(3)
        cache.add(4)
        cache.add(5)
        self.assertFalse(cache.exists(2))
