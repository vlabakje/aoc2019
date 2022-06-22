from collections import Counter

def no_double(s):
    twos = 0
    last = s[0]
    count = 1
    for c in s[1:]:
        if c == last:
            count += 1
        else:
            if count == 2:
                twos += 1
            count, last = 1, c
    if count == 2:
        twos += 1
    return twos < 1

def decreasing(s):
    last = 0
    for i in s:
        if int(i) < last:
            return True
        last = int(i)
    return False

def possible(start, end):
    for i in range(start, end+1):
        s = str(i)
        if no_double(s):
            continue
        if decreasing(s):
            continue
        yield i

print(sum(1 for i in possible(234208, 765869)))
