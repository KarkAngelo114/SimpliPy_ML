import sys
import subprocess
from .._utils import _ANSI, __pkg_ver__
from importlib.metadata import version as get_installed_version  # Python 3.8+

# Constants
PACKAGE_NAME = "SimpliPy_ML"

#Self-updating function. Call this from the main python file or whatever the name of the python file is.
#Calling this will update the library without using CMD to update SimpliPy_ML. It will check first if there's an updates from PyPi, otherwise get updates from github
def self_update():
    """
    Checks the current installed version of SimpliPy_ML and updates it if a newer version is found on PyPI. Falls back to GitHub if needed.
    """
    print("\n=================================")
    print(f"{_ANSI.cyan()}>> Checking for updates for {_ANSI.yellow()}{PACKAGE_NAME}{_ANSI.reset()}\n")

    try:
        installed_version = get_installed_version(PACKAGE_NAME)
        latest_version = __pkg_ver__.get_latest_pypi_version(PACKAGE_NAME)

        if latest_version is None:
            print(f"{_ANSI.yellow()}>> Skipping PyPI check. Trying GitHub...{_ANSI.reset()}")
        elif latest_version > installed_version:
            print(f"{_ANSI.green()}>> New version available on PyPI: {latest_version} Installed Version: ({installed_version}){_ANSI.reset()}")
            subprocess.check_call([
                sys.executable,
                "-m", "pip",
                "install",
                "--upgrade",
                PACKAGE_NAME
            ])
            print(f"{_ANSI.green()}>> Successfully updated from PyPI! Please restart the application.{_ANSI.reset()}")
            return True
        else:
            print(f"{_ANSI.cyan()}>> Already up-to-date on PyPI: {installed_version}{_ANSI.reset()}")
            return True

    except Exception as e:
        print(f"{_ANSI.yellow()}>> PyPI update failed or not available: {e}{_ANSI.reset()}")
        print(f"{_ANSI.yellow()}>> Trying to update from GitHub...{_ANSI.reset()}")
    
    print("\n=================================")

    local_version = __pkg_ver__.get_local_version()
    latest_version = __pkg_ver__.get_latest_github_version()

    if latest_version is None:
        print(f"{_ANSI.yellow()}>> Could not fetch latest version from GitHub. Skipping update.{_ANSI.reset()}")
        return False

    elif local_version is None:
        print(f"{_ANSI.yellow()}>> Local version unknown. Unable to update{_ANSI.reset()}")

    elif latest_version == local_version:
        print(f"{_ANSI.cyan()}>> Already up-to-date: {_ANSI.yellow()}{latest_version}{_ANSI.reset()}")
        return True
    
    elif latest_version != local_version:
        print(f"{_ANSI.cyan()}>> New version available: {latest_version} {_ANSI.yellow()}[Installed version: {local_version}]{_ANSI.reset()}\n")

        try:
            subprocess.check_call([
                sys.executable,
                "-m", "pip",
                "install",
                "--upgrade",
                "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
            ])
            print(f"{_ANSI.cyan()}>> Successfully updated from GitHub!{_ANSI.reset()}\n")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"{_ANSI.red()}>> Update failed from both sources: {e}{_ANSI.reset()}")
            return False

def package_install(package_name):
    """
    Installs the required libraries for SimpliPy_ML.
    If package_name is '*', installs all dependencies.
    """

    dependencies = ["tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn", 'tabulate']

    try:
        if package_name == "*":
            print("\n=================================")
            print(f"{_ANSI.cyan()}>> Installing all required libraries...{_ANSI.reset()}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn", 'tabulate'
            ])

        elif package_name.lower() in dependencies:
            print("\n=================================")
            print(f"{_ANSI.cyan()}>> Installing {package_name}...{_ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        

        if package_name != "" and package_name in dependencies:
            print(f"{_ANSI.green()}>> Successfully installed {package_name}{_ANSI.reset()}")
            return True

        elif package_name == "*":
            print(f"{_ANSI.green()}>> Successfully installed all libraries{_ANSI.reset()}")
            return True

        elif package_name != "" and package_name not in dependencies:
            print(f"{_ANSI.red()}>> {package_name} is not in it's dependencies.{_ANSI.reset()}")
            return False

       
    except subprocess.CalledProcessError as e:
        print(f"{_ANSI.red()}>> Failed to install {package_name}: {e}{_ANSI.reset()}")
        return False