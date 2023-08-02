# Subtract with Borrow
def sbb(a, b, borrow):
    # Compute a - (b + borrow) as a 128-bit integer
    ret = (a - (b + (borrow >> 63))) & ((1 << 128) - 1)

    # Extract the lower 64 bits as the result and the upper 64 bits as the new borrow
    result = ret & ((1 << 64) - 1)
    new_borrow = (ret >> 64) & ((1 << 64) - 1)

    return result, new_borrow


# Multiply and Add with Carry
def mac(a, b, c, carry):
    # Compute a + (b * c) + carry as a 128-bit integer
    ret = (a + (b * c) + carry) & ((1 << 128) - 1)

    # Extract the lower 64 bits as the result and the upper 64 bits as the new carry over
    result = ret & ((1 << 64) - 1)
    new_carry = (ret >> 64) & ((1 << 64) - 1)

    return result, new_carry


# Add with Carry
def adc(a, b, carry):
    ret = a + b + carry
    return (ret & ((1 << 64) - 1), (ret >> 64) & ((1 << 64) - 1))
