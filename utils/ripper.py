
"""
Парсер скобочного формата.
"""

def parse(src, pos=0):
    list = []
    pos += 1
    chr = src[pos]
    if chr == '\n':
        pos += 1
        chr = src[pos]
    beg = pos
    while True:
        if chr == "{":
            sub, pos = parse(src, pos)
            list.append(sub)
            pos += 1
            chr = src[pos]
            if chr == '\n':
                pos += 1
                chr = src[pos]
            beg = pos
        elif chr == ",":
            if beg < pos:
                list.append(src[beg:pos])
            pos += 1
            chr = src[pos]
            if chr == '\n':
                pos += 1
                chr = src[pos]
            beg = pos
        elif chr == "}":
            if beg < pos:
                list.append(src[beg:pos])
            break
        elif chr == '"':
            while chr == '"':
                pos += 1
                while src[pos] != '"':
                    pos += 1
                pos += 1
                chr = src[pos]
        else:
            pos += 1
            chr = src[pos]
    return list, pos