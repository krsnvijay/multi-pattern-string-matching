base = 256
mod = 101


def rolling_hash(literal):
    y = [ord(x) for x in list(literal)]
    sum = 0
    for i in range(len(y)):
        sum += y[i] * base ** i
        sum %= mod
    return sum


def string_matching():
    pattern = "dba"
    something = "ccaccaaedba"
    sum_pattern = rolling_hash(pattern)
    for i in range(len(something) - len(pattern) + 1):
        # change this
        sum_something = rolling_hash(something[i:i+len(pattern)])
        if sum_something == sum_pattern:
            if something[i:i+len(pattern)] == pattern:
                return i
    return -1


pos = string_matching()
if pos == -1:
    print("pattern not found")
else:
    print(f'pattern found at {pos} index')