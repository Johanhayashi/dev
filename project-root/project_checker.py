"""Simple project checker script."""

import os


def check_files():
    expected = ["bot.py", "agent.py", "trader.py", "watcher.py", "project_checker.py", "utils.py"]
    missing = [f for f in expected if not os.path.exists(f)]
    if missing:
        print("Missing files:", ", ".join(missing))
        return False
    print("All expected files present")
    return True


if __name__ == "__main__":
    check_files()
