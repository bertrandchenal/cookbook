# inspired by https://en.wikipedia.org/wiki/S/KEY

# Example usage:
#   $ head -c 8 /dev/urandom  | python d2048.py
#   WAIL WING BEEN GIN ICY LUCY
#   $ python d2048.py WAIL WING BEEN GIN ICY LUCY
#   ...

from os.path import abspath, dirname, join
import struct
here = abspath(dirname(__file__))

words = open(join(here, '2048.txt')).read().splitlines()
idx = dict((w, e) for e, w in enumerate(words))


def encode(payload: bytes):
    # First convert bytes into int
    base_val = struct.unpack("<Q", payload)[0]
    # Compute 2-bits checksum
    cs = base_val % 4
    # concat value & checksum
    val = (base_val << 2) + cs

    # val is now a 66 bits number and 2**11 is 2048
    res = []
    for _ in range(6):
        pos = val % 2048
        res.append(words[pos])
        val = val >> 11
    return ' '.join(res)


def decode(wordlist: [str]):
    val = 0
    while wordlist:
        w = wordlist.pop()
        # transform each word to a number and stack bits
        val += idx[w]
        if wordlist:
            val = val << 11

    # verify checksum
    assert (val >> 2 ) % 4 == val % 4
    # Convert integer to bytes
    return struct.pack("<Q", val>>2)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        sys.stdout.buffer.write(decode(sys.argv[1:]))
    else:
        data = sys.stdin.buffer.read()
        print(encode(data))
