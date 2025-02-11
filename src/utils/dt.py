import datetime
from typing import Tuple

import pytz


def get_utcdt_and_local_timezone() -> Tuple[datetime.datetime, str]:
    # Get the current time in UTC
    now_utc = datetime.datetime.now(pytz.utc)

    # Get the local time
    local_time = now_utc.astimezone()

    # Get the timezone name
    timezone_name = local_time.tzname()
    return now_utc, timezone_name
