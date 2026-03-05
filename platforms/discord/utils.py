"""
Discord ユーティリティ
"""

import logging
from datetime import datetime

import discord
from zoneinfo import ZoneInfo

from core.wrapup import CollectedMessages, WRAPUP_CHAR_CAP

logger = logging.getLogger("discord_bot")
JST = ZoneInfo("Asia/Tokyo")


def make_discord_collector(guild: discord.Guild):
    """Discord Guild 用のメッセージ収集関数を返す。"""

    async def collect(after_dt: datetime, before_dt: datetime) -> CollectedMessages:
        parts: dict[str, list[str]] = {}
        total_chars = 0
        total_msgs = 0
        truncated = False

        for text_ch in guild.text_channels:
            if truncated:
                break
            ch_label = text_ch.name
            try:
                async for msg in text_ch.history(after=after_dt, before=before_dt, oldest_first=True):
                    if not msg.content:
                        continue
                    ts = msg.created_at.astimezone(JST).strftime("%Y-%m-%d %H:%M")
                    line = f"[{ts}] {msg.author.display_name}: {msg.content}"
                    total_chars += len(line) + 1
                    total_msgs += 1
                    parts.setdefault(ch_label, []).append(line)
                    if total_chars >= WRAPUP_CHAR_CAP:
                        truncated = True
                        break
            except discord.Forbidden:
                logger.debug("wrapup: no permission for #%s (%d)", text_ch.name, text_ch.id)
            except Exception as e:
                logger.warning("wrapup: error fetching #%s: %s", text_ch.name, e)

        return CollectedMessages(parts, total_chars, total_msgs, truncated)

    return collect


def get_guild_channels(guild: discord.Guild) -> list[tuple[int, str]]:
    """ギルドのテキストチャンネル + スレッドを (id, name) のリストで返す。"""
    channels: list[tuple[int, str]] = []
    for ch in guild.channels:
        if isinstance(ch, discord.TextChannel):
            channels.append((ch.id, ch.name))
    for th in guild.threads:
        if isinstance(th.parent, discord.TextChannel):
            channels.append((th.id, f"{th.parent.name} > {th.name}"))
    channels.sort(key=lambda x: x[1])
    return channels
