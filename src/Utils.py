from datetime import timedelta
from typing import List

def formatTimeDelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())

    days, remainder = divmod(total_seconds, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{days}d {hours}h {minutes}m {seconds}s'