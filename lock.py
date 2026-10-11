import random
from fractions import Fraction

class LinearEquation:
    def __init__( self, key: int, number_range = (-1000, 1000)):
        self.min_num, self.max_num = number_range

        while True:
            self.left = self.generate_side()
            self.right = self.generate_side()

            left_k = self.get_key_coefficient(self.left)
            right_k = self.get_key_coefficient(self.right)

            # 일차방정식 조건
            if left_k == right_k:
                continue

            constants = self.get_constant_terms()

            # 보정량을 나눠 가질 상수항이 있어야 함
            if len(constants) == 0:
                continue

            self.distribute(constants, key, left_k, right_k)

            # 조정 후 0 이 된 상수항이 없어야 함
            if all(term["value"] != 0 for term, _ in constants):
                break

        self.value = self.make_value()

    def __str__(self):
        return " ".join(str(t) for t in self.value)

    def nonzero_randint(self, a, b):
        while True:
            num = random.randint(a, b)
            if num != 0:
                return num

    def rand(self):
        return self.nonzero_randint(self.min_num, self.max_num)

    def random_fraction(self):
        numerator = self.nonzero_randint(-100, 100)
        denominator = self.nonzero_randint(-50, 50)

        return Fraction(numerator, denominator)


    def generate_term(self):
        is_constant = random.choice([True, False])

        if is_constant:
            return {
                "kind": "const",
                "value": self.rand(),
            }
        else:
            coefficient_is_fraction = random.choice([True, False])
            if coefficient_is_fraction:
                return {
                    "kind": "unknown",
                    "coefficient": self.random_fraction()
                }
            else:
                return {
                    "kind": "unknown",
                    "coefficient": self.nonzero_randint(-20, 50)
                }


    def generate_side(self):
        count = random.randint(5, 10)

        terms = []

        for _ in range(count):
            terms.append(
                self.generate_term()
            )

        self.fix_fraction_sum(terms)

        return terms

    def fix_fraction_sum(self, side):
        # 이 변의 분수 계수 합이 정수가 되도록 두 개씩 짝지어 조정
        fractions = []

        for term in side:
            if term["kind"] == "unknown" and Fraction(term["coefficient"]).denominator != 1:
                fractions.append(term)

        for i in range(0, len(fractions) - 1, 2):
            first = fractions[i]["coefficient"]
            second = fractions[i + 1]["coefficient"]

            n = round(first + second)
            fractions[i + 1]["coefficient"] = n - first

        # 짝이 없는 하나는 0 이 아닌 정수로 반올림
        if len(fractions) % 2 == 1:
            last = fractions[-1]
            n = round(last["coefficient"])

            if n == 0:
                n = 1 if last["coefficient"] > 0 else -1

            last["coefficient"] = n

    def get_constant_terms(self):
        # (항, 부호) 좌변은 1, 우변은 -1
        result = []

        for term in self.left:
            if term["kind"] == "const":
                result.append((term, 1))

        for term in self.right:
            if term["kind"] == "const":
                result.append((term, -1))

        return result


    def distribute(self, constants, key, left_k, right_k):
        left_c = self.get_constant(self.left)
        right_c = self.get_constant(self.right)

        # key 를 대입했을 때 (좌변 - 우변) 값
        diff = int((left_k - right_k) * key + left_c - right_c)

        share, remainder = divmod(diff, len(constants))

        amounts = []

        for i in range(len(constants)):
            amounts.append(share + (1 if i < remainder else 0))

        # 균등하게 나누면 상수들의 앞자리가 같아지므로 합은 유지하면서 섞음
        spread = abs(share) * 3

        for i in range(len(amounts)):
            j = random.randrange(len(amounts))
            t = random.randint(-spread, spread)

            amounts[i] += t
            amounts[j] -= t

        for (term, sign), amount in zip(constants, amounts):
            term["value"] -= sign * amount

    def term_value(self, term):
        match term["kind"]:
            case "const":
                return term["value"]
            case "unknown":
                return term["coefficient"]


    def token_fraction(self, value):
        if value.denominator == 1:
            return [value.numerator]

        return [
            "(",
            value.numerator,
            "/",
            value.denominator,
            ")"
        ]


    def token_term(self, term):
        value = abs(Fraction(self.term_value(term)))
        tokens = self.token_fraction(value)

        if term["kind"] == "unknown":
            tokens.append("k")

        return tokens

    def token_side(self, side):
        result = []

        for i, term in enumerate(side):
            if self.term_value(term) < 0:
                result.append("-")
            elif i != 0:
                result.append("+")

            result += self.token_term(term)

        return result

    def get_key_coefficient(self, side):
        total = Fraction(0)

        for term in side:
            if term["kind"] == "unknown":
                total += term["coefficient"]

        return total

    def get_constant(self, side):
        total = Fraction(0)

        for term in side:
            if term["kind"] == "const":
                total += term["value"]

        return total

    def make_value(self):
        return (
            self.token_side(self.left)
            +
            ["="]
            +
            self.token_side(self.right)
        )

with open("secret.md", "r", encoding="utf-8") as f:
    s = f.read()

chars = []

for ch in s:
    chars.append(ord(ch))

try:
    KEY = int(input("KEY: "))
except Exception:
    KEY = random.randint(0, 10000)

linear = LinearEquation(key=KEY, number_range=(-100000000, 100000000))

front = []

for v in linear.value:
    if type(v) == int:
        front.append(hex(v))
    else:
        front.append(hex(ord(v)))

front = "".join(front)

back = []

for num in chars:
    back.append(hex(num - KEY))

back = "".join(back)

r = f"{front}\0{back}"

with open("secret-locked.txt", "w", encoding="utf-8") as f:
    f.write(r)
