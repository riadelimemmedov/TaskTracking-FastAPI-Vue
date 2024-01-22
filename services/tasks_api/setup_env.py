from typing import Any

from decouple import Config, RepositoryEnv

DOTENV_FILE = "./.env.development"
env_config = Config(RepositoryEnv(DOTENV_FILE))


def load_env(key: str, cast: Any = None):
    return env_config.get(key, cast=cast)
