import unittest

from fizzbuzz import fizzbuzz, fizzbuzz_range


class TestFizzbuzz(unittest.TestCase):
    """Tests for the *fizzbuzz* single-value function."""

    def test_regular_number(self):
        self.assertEqual(fizzbuzz(1), "1")
        self.assertEqual(fizzbuzz(2), "2")
        self.assertEqual(fizzbuzz(4), "4")
        self.assertEqual(fizzbuzz(7), "7")
        self.assertEqual(fizzbuzz(11), "11")

    def test_fizz(self):
        self.assertEqual(fizzbuzz(3), "Fizz")
        self.assertEqual(fizzbuzz(6), "Fizz")
        self.assertEqual(fizzbuzz(9), "Fizz")
        self.assertEqual(fizzbuzz(12), "Fizz")

    def test_buzz(self):
        self.assertEqual(fizzbuzz(5), "Buzz")
        self.assertEqual(fizzbuzz(10), "Buzz")
        self.assertEqual(fizzbuzz(20), "Buzz")

    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(15), "FizzBuzz")
        self.assertEqual(fizzbuzz(30), "FizzBuzz")
        self.assertEqual(fizzbuzz(45), "FizzBuzz")

    def test_zero(self):
        # 0 is divisible by every non-zero integer
        self.assertEqual(fizzbuzz(0), "FizzBuzz")


class TestFizzbuzzRange(unittest.TestCase):
    """Tests for the *fizzbuzz_range* convenience function."""

    def test_first_twenty(self):
        expected = [
            "1", "2", "Fizz", "4", "Buzz",
            "Fizz", "7", "8", "Fizz", "Buzz",
            "11", "Fizz", "13", "14", "FizzBuzz",
            "16", "17", "Fizz", "19", "Buzz",
        ]
        self.assertEqual(fizzbuzz_range(1, 20), expected)

    def test_single_element(self):
        self.assertEqual(fizzbuzz_range(3, 3), ["Fizz"])
        self.assertEqual(fizzbuzz_range(5, 5), ["Buzz"])
        self.assertEqual(fizzbuzz_range(1, 1), ["1"])

    def test_range_including_zero(self):
        self.assertEqual(fizzbuzz_range(0, 3), ["FizzBuzz", "1", "2", "Fizz"])

    def test_reverse_range(self):
        # end < start should produce an empty list
        self.assertEqual(fizzbuzz_range(10, 1), [])


if __name__ == "__main__":
    unittest.main()
