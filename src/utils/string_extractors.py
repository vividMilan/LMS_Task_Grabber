def split_viva_times(input: str) -> str:
    return input.split(":", 1)[1].strip()
