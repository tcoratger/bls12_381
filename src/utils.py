def sbb(a, b, borrow):
    """
    The function `sbb` subtracts `b` and `borrow` from `a` and returns the lower 64 bits of the result
    as well as the upper 64 bits as the new borrow.

    :param a: The parameter "a" represents the first 128-bit integer in the subtraction operation
    :param b: The parameter "b" represents the value to be subtracted from "a" in the function sbb
    :param borrow: The parameter "borrow" is used to indicate whether there is a borrow from a previous
    subtraction operation. It is a 64-bit integer that represents the borrow value
    :return: two values: the result and the new borrow.
    """
    # Compute a - (b + borrow) as a 128-bit integer
    ret = (a - (b + (borrow >> 63))) & ((1 << 128) - 1)

    # Extract the lower 64 bits as the result and the upper 64 bits as the new borrow
    result = ret & ((1 << 64) - 1)
    new_borrow = (ret >> 64) & ((1 << 64) - 1)

    return result, new_borrow


def mac(a, b, c, carry):
    """
    The function `mac` computes the sum of three 64-bit integers (`a`, `b`, `c`) and a carry value, and
    returns the lower 64 bits of the result as well as the upper 64 bits as the new carry value.

    :param a: The parameter "a" represents the first 64 bits of a 128-bit integer
    :param b: The parameter "b" represents a 64-bit integer value
    :param c: The parameter `c` represents a 64-bit integer value
    :param carry: The `carry` parameter represents the carry-over value from the previous calculation.
    It is used to add to the result of the current calculation
    :return: a tuple containing the lower 64 bits of the computed value as the first element and the
    upper 64 bits as the second element.
    """
    # Compute a + (b * c) + carry as a 128-bit integer
    ret = (a + (b * c) + carry) & ((1 << 128) - 1)

    # Extract the lower 64 bits as the result and the upper 64 bits as the new carry over
    result = ret & ((1 << 64) - 1)
    new_carry = (ret >> 64) & ((1 << 64) - 1)

    return result, new_carry


def adc(a, b, carry):
    """
    The function `adc` performs addition of two numbers `a` and `b` along with a carry value.

    :param a: The parameter "a" represents the first number to be added in the addition operation
    :param b: The parameter "b" in the function "adc" represents the second operand of the addition
    operation
    :param carry: The carry parameter is used to represent the carry bit in addition. It is a binary
    value that indicates whether there is a carry from the previous addition operation
    :return: The function `adc` returns a tuple containing two values. The first value is the sum of
    `a`, `b`, and `carry`, masked to 64 bits. The second value is the carry bit resulting from the
    addition, also masked to 64 bits.
    """
    ret = a + b + carry
    return (ret & ((1 << 64) - 1), (ret >> 64) & ((1 << 64) - 1))


def wrapping_mul_u64(a, b):
    """
    The function `wrapping_mul_u64` performs a multiplication of two 64-bit unsigned integers and
    returns the result modulo 2^64.

    :param a: The parameter "a" is a 64-bit unsigned integer
    :param b: The parameter "b" is a 64-bit unsigned integer
    :return: the result of multiplying `a` and `b`, and then performing a bitwise AND operation with the
    value `(1 << 64) - 1`. This operation is used to ensure that the result is wrapped within a 64-bit
    unsigned integer range.
    """
    return (a * b) & ((1 << 64) - 1)
