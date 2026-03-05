"""
プラットフォーム抽象化の基底クラスとコンテキスト
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PlatformContext:
    """プラットフォーム固有の実行コンテキスト。"""
    name: str                                   # "discord" | "slack" | "notion"
    workspace_dir: Path                         # platforms/{name}/workspace/
    capabilities: frozenset[str] = field(       # {"embed", "reaction", "thread", ...}
        default_factory=frozenset,
    )
    format_hint: str = ""                       # 出力形式ヒント（Discordマークダウン制約等）
    disabled_skills: frozenset[str] = field(    # このプラットフォームで無効なスキル名
        default_factory=frozenset,
    )


class PlatformAdapter(ABC):
    """プラットフォーム固有の起動・実行を抽象化する基底クラス。"""

    def __init__(self, context: PlatformContext):
        self.context = context

    @abstractmethod
    async def start(self) -> None:
        """プラットフォームのボット/クライアントを起動する。"""

    @abstractmethod
    async def stop(self) -> None:
        """プラットフォームのボット/クライアントを停止する。"""
