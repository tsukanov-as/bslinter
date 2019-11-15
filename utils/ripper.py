
"""
Парсер скобочного формата.
"""

def parse(src, pos=0):
    list = []
    pos = pos + 1
    chr = src[pos]
    if chr == '\n':
        pos = pos + 1
        chr = src[pos]
    beg = pos
    while True:
        if chr == "{":
            sub, pos = parse(src, pos)
            list.append(sub)
            pos = pos + 1
            chr = src[pos]
            if chr == '\n':
                pos = pos + 1
                chr = src[pos]
            beg = pos
        elif chr == ",":
            if beg < pos:
                list.append(src[beg:pos])
            pos = pos + 1
            chr = src[pos]
            if chr == '\n':
                pos = pos + 1
                chr = src[pos]
            beg = pos
        elif chr == "}":
            if beg < pos:
                list.append(src[beg:pos])
            break
        elif chr == '"':
            while chr == '"':
                pos = pos + 1
                while src[pos] != '"':
                    pos = pos + 1
                pos = pos + 1
                chr = src[pos]
        else:
            pos = pos + 1
            chr = src[pos]
    return list, pos