import urllib.request
from . import _ANSI
import os
import sys
import json

if not any("__main__" in module for module in sys.modules):
    raise ImportError("This module is for internal use only and cannot be imported directly.")

# GitHub raw URL to the VERSION.txt file
VERSION_FILE_URL = "https://raw.githubusercontent.com/KarkAngelo114/SimpliPy_ML/main/SimpliPy_ML/_utils/VERSION.txt"


# Utility to get installed version (if __version__ isn't available, fallback to custom solution)
def get_local_version():
    # Fallback to reading from bundled VERSION.txt
    try:
        # Get the path to the VERSION.txt inside the installed package
        version_file = os.path.join(os.path.dirname(__file__), "VERSION.txt")
        with open(version_file, "r") as version_reader:
            return version_reader.read().strip()
    except Exception:
        return None

# Get latest version from GitHub VERSION.txt
def get_latest_github_version():
    try:
        with urllib.request.urlopen(VERSION_FILE_URL) as response:
            return response.read().decode().strip()
    except Exception as e:
        print(f"{_ANSI.yellow()}>> Could not fetch latest version from GitHub: {e}{_ANSI.reset()}")
        return None

# function to get package version from PyPi
def get_latest_pypi_version(package_name):
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package_name}/json") as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception as e:
        print(f"{_ANSI.yellow()}>> Could not fetch latest version from PyPI: {e}{_ANSI.reset()}")
        return None