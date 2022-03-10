"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time
import math


class BinaryNumber:
    """ done """

    def __init__(self, n):
        self.decimal_val = n
        self.binary_vec = list('{0:b}'.format(n))

    def __repr__(self):
        return ('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))


## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec):
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))


def split_number(vec):
    return (binary2int(vec[:len(vec) // 2]),
            binary2int(vec[len(vec) // 2:]))


def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)


def pad(x, y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y) - len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x) - len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x, y


def _subquadratic_multiply(x, y):
    # this just converts the result from a BinaryNumber to a regular int
    return subquadratic_multiply(x, y).decimal_val


def subquadratic_multiply(x, y):
    xVec = x.binary_vec
    yVec = y.binary_vec
    xVec, yVec = pad(xVec, yVec)
    m = len(yVec)

    if x.decimal_val < 2 or y.decimal_val < 2:
        return BinaryNumber(x.decimal_val * y.decimal_val)

    xL, xR = split_number(xVec)
    yL, yR = split_number(yVec)

    z0 = subquadratic_multiply(xR, yR)
    z1 = subquadratic_multiply(BinaryNumber(xL.decimal_val + xR.decimal_val),
                               BinaryNumber(yL.decimal_val + yR.decimal_val))
    z2 = subquadratic_multiply(xL, yL)
    '''
    z0 = karatsuba (low1, low2)
    z1 = karatsuba (low1 + high1, low2 + high2)
    z2 = karatsuba (high1, high2)
    return (z2 × 10 ^ (m2 × 2)) + ((z1 - z2 - z0) × 10 ^ m2) + z0
    
    XY = 2^2ceil(n/2) XlYl + 2^ceil(n/2) * [(Xl + Xr)(Yl + Yr) - XlYl - XrYr] + XrYr
    '''
    return BinaryNumber((BinaryNumber(bit_shift(z2, 2 * (m // 2)).decimal_val + bit_shift(
        BinaryNumber(z1.decimal_val - z2.decimal_val - z0.decimal_val),
        m // 2).decimal_val + z0.decimal_val).decimal_val))




# Feel free to add your own tests here.
def test_multiply():
    #x = 100000
    #print(time_multiply(x, x, subquadratic_multiply))
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2 * 2
    assert subquadratic_multiply(BinaryNumber(10000), BinaryNumber(2)).decimal_val == 10000 * 2


def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    time.sleep(0.025)

    f(BinaryNumber(x), BinaryNumber(y))

    return (time.time() - start - 0.025) * 1000





