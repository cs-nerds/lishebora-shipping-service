import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_code() -> str:
    return str(random.randint(0, 1000))


def random_currency() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=3))


def random_longitude() -> float:
    return random.random() * random.choice([180, 180])


def random_latitude() -> float:
    return random.random() * random.choice([90, -90])
