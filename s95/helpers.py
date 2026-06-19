def min_to_mmss(m) -> str:
    """Convert decimal minutes to 'mm:ss' string format.

    Uses a tolerance of ~1 second (1/60 min) to decide whether to round
    to the nearest whole minute or floor the value.

    Example:
        >>> min_to_mmss(17.0)
        '17:00'
        >>> min_to_mmss(19.25)
        '19:15'
        >>> min_to_mmss(59.98333)
        '59:59'
    """
    mins = round(m) if abs(m - round(m)) < 0.0166665 else int(m)
    return f'{mins}:{round((m - mins) * 60):02d}'


def mmss_to_min(time_str: str) -> float:
    """Convert a 'mm:ss' or 'h:mm:ss' time string to decimal minutes.

    Parses common time formats used in race results and returns the
    equivalent value in minutes as a float. Accepts:
      - 'mm:ss'        (e.g. '23:45'  -> 23.75)
      - 'h:mm:ss'      (e.g. '1:23:45' -> 83.75)
      - 'm:ss'         (e.g. '3:45'   -> 3.75)

    Args:
        time_str: A string in one of the recognised time formats.

    Returns:
        The time expressed as decimal minutes.

    Raises:
        ValueError: If the input string cannot be parsed.

    Example:
        >>> mmss_to_min('23:45')
        23.75
        >>> mmss_to_min('1:23:45')
        83.75
        >>> mmss_to_min('3:45')
        3.75
    """
    parts = time_str.strip().split(':')

    if len(parts) == 2:
        # mm:ss or m:ss
        minutes, seconds = parts
        return int(minutes) + int(seconds) / 60
    elif len(parts) == 3:
        # h:mm:ss
        hours, minutes, seconds = parts
        return int(hours) * 60 + int(minutes) + int(seconds) / 60
    else:
        raise ValueError(
            f"Unable to parse time string '{time_str}'. "
            "Expected format: 'mm:ss' or 'h:mm:ss'"
        )
