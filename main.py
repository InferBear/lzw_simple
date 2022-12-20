def byte_reader(filename):
    with open(filename, 'rb') as f:
        while byte := f.read(1):
            yield byte


def _16_bits_int_reader(filename):
    with open(filename, 'rb') as f:
        while byte := f.read(2):
            t = int(byte[0]) * 256 + int(byte[1])
            yield t


def compress(filename, output):
    d = dict()
    for i in range(256):
        d[(i,)] = i
    max_len = 2 ** 16

    def write_16_bits(f, b):
        f.write(bytes([(b & 0xFF00) >> 8]))
        f.write(bytes([(b & 0xFF)]))

    s = tuple()
    with open(output, 'wb') as file:
        for i in byte_reader(filename):
            c = s + tuple(i)
            if c in d:
                s = c
            else:
                write_16_bits(file, d[s])
                if len(d) < max_len:
                    d[c] = len(d)
                s = tuple(i)
        if len(s) != 0:
            write_16_bits(file, d[s])


def write_file_bytes(file, byte_tuple):
    file.write(bytearray(byte_tuple))


def decompress(filename, dst):
    d = dict()
    for i in range(256):
        d[i] = (i,)
    max_len = 2 ** 16

    g = _16_bits_int_reader(filename)
    pre = d[next(g)]
    s = (pre[0],)
    with open(dst, "wb") as file:
        write_file_bytes(file, pre)
        s = tuple(bytes(s))
        for i in g:
            if i in d:
                c = d[i]
            else:
                c = s + (s[0],)
            write_file_bytes(file, c)
            if len(d) < max_len:
                d[len(d)] = s + (c[0],)
            s = c


if __name__ == '__main__':
    compress("bible.txt", "output")
    decompress("output", "result.txt")
