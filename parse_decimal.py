from decimal import Decimal


def parse_decimal(toparse: str, precision: int) -> Decimal:
    if precision < 0:
        raise ValueError(f"precision {precision} cannot be negative")

    parts = toparse.split(".")
    if len(parts) > 2 or len(parts) < 1:
        raise ValueError(
            f"Value {toparse} cannot be parsed as a number with optional decimal"
        )
    result = Decimal(parts[0])
    if len(parts) == 2 and precision > 0:
        truncated = parts[1][0:precision]
        decimal_value = Decimal(truncated) / 10 ** len(truncated)
        result += decimal_value
    return result
