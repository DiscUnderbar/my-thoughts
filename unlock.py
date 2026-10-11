import re
from fractions import Fraction

def parse_hex_stream(s):
    result = []

    i = 0

    while i < len(s):

        negative = False

        if s[i:i+3] == "-0x":
            negative = True
            i += 3

        elif s[i:i+2] == "0x":
            i += 2

        else:
            i += 1
            continue


        start = i

        while i < len(s):

            # 다음 토큰 시작
            if s[i:i+2] == "0x":
                break

            if s[i:i+3] == "-0x":
                break

            i += 1


        value = int(s[start:i], 16)

        if negative:
            value = -value

        result.append(value)


    return result

def decode_front(values):
    """
    LinearEquation의 token 복원
    """
    symbols = {
        40: "(",
        41: ")",
        43: "+",
        45: "-",
        47: "/",
        61: "=",
        107: "k",
    }

    result = []

    for v in values:
        if v in symbols:
            result.append(symbols[v])
        else:
            result.append(str(v))

    return result



def parse_fraction(tokens, index):
    if tokens[index] == "(":
        a = int(tokens[index + 1])
        b = int(tokens[index + 3])

        return Fraction(a, b), index + 5

    return Fraction(int(tokens[index])), index + 1



def parse_side(tokens):
    k = Fraction(0)
    c = Fraction(0)

    i = 0
    sign = 1

    while i < len(tokens):

        if tokens[i] == "+":
            sign = 1
            i += 1
            continue

        if tokens[i] == "-":
            sign = -1
            i += 1
            continue


        value, i = parse_fraction(tokens, i)

        if i < len(tokens) and tokens[i] == "k":
            k += sign * value
            i += 1
        else:
            c += sign * value

        sign = 1

    return k, c



with open(
    "secret-locked.txt",
    "r",
    encoding="utf-8"
) as f:
    data = f.read()



front, back = data.split("\0", 1)



# -----------------------
# KEY 찾기
# -----------------------

front_values = parse_hex_stream(front)

tokens = decode_front(front_values)


if "=" not in tokens:
    raise Exception("Equation not found")


equal_index = tokens.index("=")


left = tokens[:equal_index]
right = tokens[equal_index + 1:]


left_k, left_c = parse_side(left)
right_k, right_c = parse_side(right)



if left_k == right_k:
    raise Exception("Invalid equation")



KEY = (right_c - left_c) / (left_k - right_k)


if KEY.denominator != 1:
    raise Exception("KEY is not integer")


KEY = KEY.numerator


print("KEY:", KEY)



# -----------------------
# 내용 복구
# -----------------------

encrypted = parse_hex_stream(back)

result = []

for value in encrypted:
    result.append(chr(value + KEY))



with open(
    "secret-unlocked.md",
    "w",
    encoding="utf-8"
) as f:
    f.write("".join(result))


print("unlock complete")