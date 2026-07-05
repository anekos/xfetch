def format_price(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)
