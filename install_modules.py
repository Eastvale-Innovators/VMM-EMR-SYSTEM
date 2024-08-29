import subprocess
import sys

PACKAGES = ["flask", "markupsafe"]

def install(packages: list[str]):
    command = [sys.executable, "-m", "pip", "install"] + packages
    subprocess.check_call(command)

install(PACKAGES)
