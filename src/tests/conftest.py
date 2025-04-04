from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope="session")
def load_local_dev_env():
    import os
    import sys

    from dotenv import load_dotenv

    python_path = Path(__file__).resolve().parent.parent
    env_file = python_path.parent / ".env"
    sys.path.append(str(python_path))
    if env_file.exists() and env_file.is_file():
        load_dotenv(env_file)
        return True
    return False
