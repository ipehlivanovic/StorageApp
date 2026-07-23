import os
import shutil
from pathlib import Path


def pytest_configure(config):
    os.environ["DATABASE_URL"] = "sqlite:///file:memdb1?mode=memory&cache=shared"


def pytest_sessionfinish(session, exitstatus):
    """Clean up after tests and dispose engine."""
    root = Path(session.config.rootdir)

    # 1. Dispose the engine to close all connections
    from app.database import engine
    engine.dispose()
    print("\n\nEngine disposed, connections closed.")

    # 2. Delete SQLite shared memory files
    for pattern in ["file", "file-shm", "file-wal"]:
        file_path = root / pattern
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed shared memory test database: {file_path}")
            except Exception as e:
                print(f"Could not remove {file_path}: {e}")
                pass

    print("--- Running automatic cache cleanup ---")

    # 3. Clean pycache and pytest_cache
    ignored_folders = {".venv", "venv", ".git", "env"}
    for cache_dir in root.rglob("__pycache__"):
        # Check if any parent folder is in the ignored list
        if any(part in ignored_folders for part in cache_dir.parts):
            continue

        try:
            shutil.rmtree(cache_dir)
        except Exception:
            pass

    # 4. Clear .pytest_cache folder safely
    pytest_cache = root / ".pytest_cache"
    if pytest_cache.exists():
        try:
            shutil.rmtree(pytest_cache)
        except Exception:
            pass
