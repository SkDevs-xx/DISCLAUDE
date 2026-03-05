"""
定数・設定管理・スケジュール/テンプレート/チャンネル名の読み書き
"""

import json
import logging
import os
import shutil
import tempfile
from pathlib import Path

# ─────────────────────────────────────────────
# 定数
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
WORKFLOW_DIR = BASE_DIR / "workspace"
MEMORY_DIR = WORKFLOW_DIR / "memory"
SCHEDULES_FILE = WORKFLOW_DIR / "schedules" / "schedules.json"
ATTACHMENTS_DIR = WORKFLOW_DIR / "temp"
TMP_DIR = WORKFLOW_DIR / "temp"
CONFIG_FILE = BASE_DIR / "config.json"
PLATFORM_NAME: str = ""                         # "discord" | "slack" | "notion"
SOUL_FILE = WORKFLOW_DIR / "SOUL.md"
USER_FILE = WORKFLOW_DIR / "USER.md"
CHANNEL_NAMES_FILE = WORKFLOW_DIR / "channel_names.json"
SESSIONS_FILE = WORKFLOW_DIR / "sessions.json"
CLAUDE_MD_FILE = BASE_DIR / "CLAUDE.md"
LOG_FILE = BASE_DIR / "bot.log"

def init_workspace(workspace_dir: Path) -> None:
    """起動時にプラットフォーム固有の workspace パスを設定する。"""
    global WORKFLOW_DIR, MEMORY_DIR, SCHEDULES_FILE, ATTACHMENTS_DIR, TMP_DIR
    global CHANNEL_NAMES_FILE, SESSIONS_FILE, SOUL_FILE, USER_FILE
    global PLATFORM_NAME
    WORKFLOW_DIR = workspace_dir
    MEMORY_DIR = WORKFLOW_DIR / "memory"
    SCHEDULES_FILE = WORKFLOW_DIR / "schedules" / "schedules.json"
    ATTACHMENTS_DIR = WORKFLOW_DIR / "temp"
    TMP_DIR = WORKFLOW_DIR / "temp"
    CHANNEL_NAMES_FILE = WORKFLOW_DIR / "channel_names.json"
    SESSIONS_FILE = WORKFLOW_DIR / "sessions.json"
    SOUL_FILE = WORKFLOW_DIR / "SOUL.md"
    USER_FILE = WORKFLOW_DIR / "USER.md"
    # platforms/{name}/workspace/ の親ディレクトリ名がプラットフォーム名
    PLATFORM_NAME = workspace_dir.parent.name


CLAUDE_BIN = shutil.which("claude") or str(Path.home() / ".local" / "bin" / "claude")
TIMEOUT_FAST = 180
TIMEOUT_PLANNING = 300

logger = logging.getLogger("discord_bot")


def _atomic_write_json(path: Path, data) -> None:
    """tempfile + os.rename で JSON を安全に書き込む。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ─────────────────────────────────────────────
# 設定管理
# ─────────────────────────────────────────────

_config_cache: dict | None = None
_config_mtime: float = 0.0

def load_config() -> dict:
    global _config_cache, _config_mtime
    try:
        mtime = os.path.getmtime(CONFIG_FILE)
    except OSError:
        mtime = 0.0
    if _config_cache is not None and mtime == _config_mtime:
        return _config_cache
    if not CONFIG_FILE.exists():
        _config_cache = {}
        _config_mtime = 0.0
        return _config_cache
    with open(CONFIG_FILE, encoding="utf-8") as f:
        _config_cache = json.load(f)
    _config_mtime = mtime
    return _config_cache

def get_skip_permissions() -> bool:
    return load_platform_config().get("skip_permissions", True)

def save_config(cfg: dict) -> None:
    global _config_cache, _config_mtime
    _atomic_write_json(CONFIG_FILE, cfg)
    _config_cache = cfg
    _config_mtime = os.path.getmtime(CONFIG_FILE)


# ─────────────────────────────────────────────
# プラットフォーム固有設定（config.json の platforms セクション）
# ─────────────────────────────────────────────

def load_platform_config() -> dict:
    """プラットフォーム固有設定を返す。init_workspace() 前は空 dict。"""
    if not PLATFORM_NAME:
        return {}
    return load_config().get(PLATFORM_NAME, {})

def save_platform_config(cfg: dict) -> None:
    if not PLATFORM_NAME:
        logger.error("save_platform_config: PLATFORM_NAME is not set")
        return
    full_cfg = load_config()
    full_cfg[PLATFORM_NAME] = cfg
    save_config(full_cfg)

def load_schedules() -> list:
    if not SCHEDULES_FILE.exists():
        return []
    try:
        with open(SCHEDULES_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError):
        return []

def save_schedules(schedules: list) -> None:
    _atomic_write_json(SCHEDULES_FILE, schedules)

def load_channel_names() -> dict:
    if not CHANNEL_NAMES_FILE.exists():
        return {}
    try:
        with open(CHANNEL_NAMES_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}

def save_channel_name(channel_id: int, name: str) -> None:
    data = load_channel_names()
    if data.get(str(channel_id)) != name:
        data[str(channel_id)] = name
        _atomic_write_json(CHANNEL_NAMES_FILE, data)

def get_channel_name(channel_id: int) -> str:
    data = load_channel_names()
    return data.get(str(channel_id), str(channel_id))

def get_channel_session(channel_id: int) -> str | None:
    if not SESSIONS_FILE.exists():
        return None
    try:
        with open(SESSIONS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data.get(str(channel_id))
    except (json.JSONDecodeError, ValueError):
        return None

def get_model_config() -> tuple[str, bool]:
    """(model, thinking) を返す。"""
    cfg = load_platform_config()
    return cfg.get("model", "sonnet"), cfg.get("thinking", False)

def get_no_mention_channels() -> set[str]:
    return set(load_platform_config().get("no_mention_channels", []))

def set_no_mention(channel_id: int, enabled: bool) -> None:
    """enabled=True でメンション不要、False で必要に設定。"""
    cfg = load_platform_config()
    channels = list(cfg.get("no_mention_channels", []))
    cid = str(channel_id)
    if enabled and cid not in channels:
        channels.append(cid)
    elif not enabled and cid in channels:
        channels.remove(cid)
    cfg["no_mention_channels"] = channels
    save_platform_config(cfg)

def save_channel_session(channel_id: int, session_id: str) -> None:
    data: dict = {}
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {}
    data[str(channel_id)] = session_id
    _atomic_write_json(SESSIONS_FILE, data)
