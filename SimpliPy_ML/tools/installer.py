import os
import sys
import subprocess
import json
import urllib.request
from ..__utils__ import ANSI, __pkg_ver__
from importlib.metadata import version as get_installed_version  # Python 3.8+

# Constants
PACKAGE_NAME = "SimpliPy_ML"



def get_latest_pypi_version(package_name):
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package_name}/json") as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception as e:
        print(f"{ANSI.yellow()}>> Could not fetch latest version from PyPI: {e}{ANSI.reset()}")
        return None


def self_update():
    """
    Checks the current installed version of SimpliPy_ML and updates it
    if a newer version is found on PyPI. Falls back to GitHub if needed.
    """
    print("\n=================================")
    print(f"{ANSI.cyan()}>> Checking for updates for {ANSI.yellow()}{PACKAGE_NAME}{ANSI.reset()}\n")

    try:
        installed_version = get_installed_version(PACKAGE_NAME)
        latest_version = get_latest_pypi_version(PACKAGE_NAME)

        if latest_version is None:
            print(f"{ANSI.yellow()}>> Skipping PyPI check. Trying GitHub...{ANSI.reset()}")
        elif latest_version > installed_version:
            print(f"{ANSI.green()}>> New version available on PyPI: {latest_version} (Installed: {installed_version}){ANSI.reset()}")
            subprocess.check_call([
                sys.executable,
                "-m", "pip",
                "install",
                "--upgrade",
                PACKAGE_NAME
            ])
            print(f"{ANSI.green()}>> Successfully updated from PyPI! Please restart the application.{ANSI.reset()}")
            return True
        else:
            print(f"{ANSI.cyan()}>> Already up-to-date on PyPI: {installed_version}{ANSI.reset()}")
            return True

    except Exception as e:
        print(f"{ANSI.yellow()}>> PyPI update failed or not available: {e}{ANSI.reset()}")
        print(f"{ANSI.yellow()}>> Trying to update from GitHub...{ANSI.reset()}")
    
    print("\n=================================")
    print(f"{ANSI.cyan()}>> Checking for updates for {ANSI.yellow()}{PACKAGE_NAME}{ANSI.reset()}\n")

    local_version = __pkg_ver__.get_local_version()
    latest_version = __pkg_ver__.get_latest_github_version()

    if latest_version is None:
        print(f"{ANSI.yellow()}>> Could not fetch latest version from GitHub. Skipping update.{ANSI.reset()}")
        return False

    elif local_version is None:
        print(f"{ANSI.yellow()}>> Local version unknown. Unable to update{ANSI.reset()}")
    elif latest_version == local_version:
        print(f"{ANSI.cyan()}>> Already up-to-date: {ANSI.yellow()}{latest_version}{ANSI.reset()}")
        return True
    elif latest_version != local_version:
        print(f"{ANSI.green()}>> New version available: {latest_version} (Installed: {local_version}){ANSI.reset()}")

        try:
            subprocess.check_call([
                sys.executable,
                "-m", "pip",
                "install",
                "--upgrade",
                "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
            ])
            print(f"{ANSI.green()}>> Successfully updated from GitHub! Please restart the application.{ANSI.reset()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{ANSI.red()}>> Update failed from both sources: {e}{ANSI.reset()}")
            return False

def package_install(package_name):
    """
    Installs the required libraries for SimpliPy_ML.
    If package_name is '*', installs all dependencies.
    """

    dependencies = ["tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn"]

    try:
        if package_name == "*":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing all required libraries...{ANSI.reset()}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn"
            ])

        elif package_name.lower() in dependencies:
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        

        if package_name != "" and package_name in dependencies:
            print(f"{ANSI.green()}>> Successfully installed {package_name}{ANSI.reset()}")
            return True

        elif package_name == "*":
            print(f"{ANSI.green()}>> Successfully installed all libraries{ANSI.reset()}")
            return True

        elif package_name != "" and package_name not in dependencies:
            print(f"{ANSI.red()}>> {package_name} is not in it's dependencies.{ANSI.reset()}")
            return False

       
    except subprocess.CalledProcessError as e:
        print(f"{ANSI.red()}>> Failed to install {package_name}: {e}{ANSI.reset()}")
        return False