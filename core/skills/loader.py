"""
SKILL.md parser: YAML frontmatter + Markdown body.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from core.skills.models import Skill

logger = logging.getLogger("discord_bot")

_FRONTMATTER_DELIMITER = "---"


def _split_frontmatter(text: str) -> tuple[str, str]:
    """YAML frontmatter と Markdown 本文を分離する。

    Returns:
        (frontmatter_yaml, body_markdown)
    """
    stripped = text.lstrip("\n")
    if not stripped.startswith(_FRONTMATTER_DELIMITER):
        return "", text

    # 2 番目の --- を探す
    end = stripped.find(_FRONTMATTER_DELIMITER, len(_FRONTMATTER_DELIMITER))
    if end == -1:
        return "", text

    fm = stripped[len(_FRONTMATTER_DELIMITER):end].strip()
    body = stripped[end + len(_FRONTMATTER_DELIMITER):].strip()
    return fm, body


def load_skill(skill_md_path: Path) -> Skill | None:
    """SKILL.md ファイルを読み込んで Skill オブジェクトを返す。

    パースに失敗した場合は None を返す。
    """
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("Failed to read skill file %s: %s", skill_md_path, e)
        return None

    fm_text, body = _split_frontmatter(text)
    if not fm_text:
        logger.warning("No frontmatter found in %s", skill_md_path)
        return None

    try:
        meta = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        logger.warning("Invalid YAML in %s: %s", skill_md_path, e)
        return None

    if not isinstance(meta, dict):
        logger.warning("Frontmatter is not a mapping in %s", skill_md_path)
        return None

    name = meta.get("name")
    if not name:
        logger.warning("Missing 'name' in frontmatter of %s", skill_md_path)
        return None

    platforms_raw = meta.get("platforms", [])
    platforms = frozenset(str(p) for p in platforms_raw) if platforms_raw else frozenset()

    return Skill(
        name=str(name),
        description=str(meta.get("description", "")),
        instructions=body,
        source_path=skill_md_path,
        platforms=platforms,
        user_invocable=bool(meta.get("user-invocable", False)),
    )
