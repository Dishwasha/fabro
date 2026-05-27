def fizzbuzz(n: int) -> str:
    """Return the FizzBuzz string for a single integer.

    - Multiples of 3  -> "Fizz"
    - Multiples of 5  -> "Buzz"
    - Multiples of 15 -> "FizzBuzz"
    - Otherwise       -> the number as a string
    """
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def fizzbuzz_range(start: int, end: int) -> list[str]:
    """Return the FizzBuzz sequence for *start*..*end* inclusive."""
    return [fizzbuzz(i) for i in range(start, end + 1)]
