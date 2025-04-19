import subprocess
import sys
from ..__utils__ import ANSI
from ..__utils__ import __version__ as current_version
import requests 

def check_github_version():
    url = "https://raw.githubusercontent.com/KarkAngelo114/SimpliPy_ML/main/SimpliPy_ML/__version__.py"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            remote_code = r.text.strip()
            # Extract version value from file content
            exec(remote_code)
            remote_version = locals().get("__version__", None)
            return remote_version
    except Exception as e:
        print(f"Failed to fetch GitHub version: {e}")
    return None

def self_update():
    """
        Calling this function will update SimpliPy_ML
    """
    print("\n=================================")
    print(f"{ANSI.cyan()}>> Updating {ANSI.yellow()}SimpliPy_ML{ANSI.reset()}\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "SimpliPy_ML"])
        print(f"{ANSI.green()}>> Successfully updated from PyPI!{ANSI.reset()}")
        return True
    except subprocess.CalledProcessError:
        print(f"{ANSI.yellow()}>> PyPI update failed, trying GitHub...{ANSI.reset()}")
        try:
            remote_version = check_github_version()
            if remote_version and remote_version != current_version.getVersion():
                print(f"{ANSI.yellow()}>> New version available: {remote_version} (current: {current_version}){ANSI.reset()}")
                try:
                    subprocess.check_call([
                        sys.executable,
                        "-m", "pip",
                        "install",
                        "--upgrade",
                        "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
                    ])
                    print(f"{ANSI.green()}>> Successfully updated to {remote_version}!{ANSI.reset()}")
                except subprocess.CalledProcessError as e:
                    print(f"{ANSI.red()}>> Update failed: {e}{ANSI.reset()}")
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