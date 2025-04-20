import urllib.request
from . import ANSI  # Import ANSI from __utils__
import os

# GitHub raw URL to the VERSION.txt file
VERSION_FILE_URL = "https://raw.githubusercontent.com/KarkAngelo114/SimpliPy_ML/main/SimpliPy_ML/__utils__/VERSION.txt"


# Utility to get installed version (if __version__ isn't available, fallback to custom solution)
def get_local_version():
    try:
        # Try importing __version__
        from SimpliPy_ML import __version__
        return __version__
    except ImportError:
        pass

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
        print(f"{ANSI.yellow()}>> Could not fetch latest version from GitHub: {e}{ANSI.reset()}")
        return None
