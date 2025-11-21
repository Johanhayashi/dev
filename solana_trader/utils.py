"""Helpers utilitários: carregamento de .env e helpers HTTP leves."""
import os
from typing import Dict


def load_env(path: str = ".env") -> Dict[str, str]:
    env = {}
    if not os.path.exists(path):
        # fallback to environment variables
        for k, v in os.environ.items():
            env[k] = v
        return env
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    # merge with os.environ (env file takes precedence)
    merged = dict(os.environ)
    merged.update(env)
    return merged
