def no_double(s):
    return len(s) == len(set(s))

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
