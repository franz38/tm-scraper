from typing import List


def list_to_csv(l: List[any]) -> str:
    return ", ".join((str(x) if x else "null") for x in l)