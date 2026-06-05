"""Peak hours calculation helpers."""
from __future__ import annotations

from datetime import datetime, time, timedelta

import pytz

from .const import DISCO_SCHEDULES, TIMEZONE

_TZ = pytz.timezone(TIMEZONE)


def _get_schedule(disco: str, month: int) -> tuple[int, int, int, int]:
    """Return (start_h, start_m, end_h, end_m) for a disco and month."""
    for months, sh, sm, eh, em in DISCO_SCHEDULES[disco]:
        if month in months:
            return sh, sm, eh, em
    # fallback to GEPCO default
    for months, sh, sm, eh, em in DISCO_SCHEDULES["GEPCO"]:
        if month in months:
            return sh, sm, eh, em
    return 18, 0, 22, 0


def get_peak_info(disco: str) -> dict:
    """Return all peak-hour sensor values for the given disco."""
    now = datetime.now(_TZ)
    month = now.month
    sh, sm, eh, em = _get_schedule(disco, month)

    peak_start = now.replace(hour=sh, minute=sm, second=0, microsecond=0)
    peak_end = now.replace(hour=eh, minute=em, second=0, microsecond=0)

    is_peak = peak_start <= now < peak_end

    if is_peak:
        delta = peak_end - now
        time_until_end = _fmt_delta(delta)
        time_until_start = None
    else:
        if now < peak_start:
            delta = peak_start - now
        else:
            # already past today's peak — next peak is tomorrow
            tomorrow_start = peak_start + timedelta(days=1)
            delta = tomorrow_start - now
        time_until_start = _fmt_delta(delta)
        time_until_end = None

    return {
        "is_peak": is_peak,
        "tariff_period": "Peak" if is_peak else "Off-Peak",
        "time_until_peak_ends": time_until_end,
        "time_until_peak_starts": time_until_start,
        "peak_start_today": peak_start.isoformat(),
        "peak_end_today": peak_end.isoformat(),
        "disco": disco,
    }


def _fmt_delta(delta: timedelta) -> str:
    total = int(delta.total_seconds())
    if total < 0:
        total = 0
    h, rem = divmod(total, 3600)
    m, _ = divmod(rem, 60)
    return f"{h:02d}:{m:02d}"
