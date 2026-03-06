"""Clive Browser MCP Server — Chrome CDP 経由のブラウザ操作を AI に提供する。"""

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .tools import register_tools

# FastMCP の pydantic_settings がプロジェクトルートの .env を読んで
# PermissionError を起こすのを回避する。
# browser/ ディレクトリには .env がないため、一時的にそこへ移動して初期化する。
_restore_cwd = os.getcwd()
os.chdir(Path(__file__).parent)

mcp = FastMCP("clive-browser")
register_tools(mcp)

os.chdir(_restore_cwd)


def main():
    import asyncio
    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
