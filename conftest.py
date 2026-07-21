import os
import shutil
from pathlib import Path
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_test_environment():
    """Set environment variable before any tests run."""
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    yield


def pytest_sessionfinish(session, exitstatus):
    """Runs automatically after tests finish, ignoring protected folders."""
    print("\n--- Running automatic cache cleanup ---")

    root = Path(session.config.rootdir)

    # Folders you want to completely ignore
    ignored_folders = {".venv", "venv", ".git", "env"}

    # 1. Clear __pycache__ folders while skipping ignored paths
    for cache_dir in root.rglob("__pycache__"):
        # Check if any parent folder is in the ignored list
        if any(part in ignored_folders for part in cache_dir.parts):
            continue

        try:
            shutil.rmtree(cache_dir)
        except Exception:
            pass

    # 2. Clear .pytest_cache folder safely
    pytest_cache = root / ".pytest_cache"
    if pytest_cache.exists():
        try:
            shutil.rmtree(pytest_cache)
        except Exception:
            pass
