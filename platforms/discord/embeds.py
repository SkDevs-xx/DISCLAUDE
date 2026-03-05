"""
Discord Embed 生成ヘルパー
"""

import discord


def make_error_embed(msg: str) -> discord.Embed:
    return discord.Embed(title="エラー", description=msg, color=discord.Color.red())

def make_info_embed(title: str, desc: str) -> discord.Embed:
    return discord.Embed(title=title, description=desc, color=discord.Color.green())
