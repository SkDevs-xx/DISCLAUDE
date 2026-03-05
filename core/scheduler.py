"""
プラットフォーム非依存のスケジューラ・cron ユーティリティ
"""

from apscheduler.triggers.cron import CronTrigger


def infer_freq_from_cron(cron: str) -> str | None:
    """cron 式から頻度タイプを推定する。

    Returns:
        "interval" | "hourly" | "weekday" | "daily" | "weekly" | None
    """
    parts = cron.strip().split()
    if len(parts) != 5:
        return None
    m, h, dom, mon, dow = parts
    if m.startswith("*/"):
        return "interval"
    if h == "*" and dom == "*" and mon == "*" and dow == "*":
        return "hourly"
    if dom == "*" and mon == "*" and dow == "MON-FRI":
        return "weekday"
    if dom == "*" and mon == "*" and dow == "*":
        return "daily"
    if dom == "*" and mon == "*":
        return "weekly"
    return None


def validate_cron(cron: str) -> bool:
    """cron 式が有効かどうかを検証する。"""
    try:
        CronTrigger.from_crontab(cron)
        return True
    except (ValueError, KeyError):
        return False
