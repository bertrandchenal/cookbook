import bisect
prefixes = 'yzafpnum_kMGTPEZY'
factors = [1000**i for i in range(-8, 8)]


def fmt(number):
    if number == 0:
        return 0
    if number < 0:
        return '-' + fmt(-number)
    idx = bisect.bisect_right(factors, number) - 1
    prefix = prefixes[idx]
    return '%.2f%s' % (number / factors[idx], '' if prefix == '_' else prefix)


def test():
    for i in range(12):
        n = i * 10**i
        print('%.2E' % n, fmt(n))
    print('--')
    for i in range(0, -12, -1):
        n = -i * 10**i
        print('%E' % n ,fmt(n))
    print('--')
    print(fmt(-90000))


if __name__ == '__main__':
    test()
