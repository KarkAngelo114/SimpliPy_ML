import os
import subprocess
import sys
from ..__utils__ import ANSI
import venv

def get_project_root():
    """
    Attempts to find the project root directory by looking for a marker file/directory.
    Adjust the marker (e.g., '.git', '.venv', or a specific file) as needed for your project.
    """
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    while True:
        if os.path.exists(os.path.join(current_dir, ".venv")):  # Look for the virtual environment directory
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached the root of the filesystem
            return None
        current_dir = parent_dir

def self_update():
    """
    Calling this function will update SimpliPy_ML to newer versions available.
    Ensures pip is executed within the project's virtual environment.
    """

    print("\n=================================")
    print(f"{ANSI.cyan()}>> Updating {ANSI.yellow()}SimpliPy_ML{ANSI.reset()}\n")

    original_cwd = os.getcwd()

    try:
        project_root = get_project_root()
        if not project_root:
            print(f"{ANSI.yellow()}>> Could not determine the project root directory.{ANSI.reset()}")
            return False

        venv_path = os.path.join(project_root, ".venv")

        pip_executable = os.path.join(venv_path, "bin", "pip")
        if sys.platform == "win32":
            pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")

        if not os.path.exists(pip_executable):
            print(f"{ANSI.yellow()}>> Virtual environment not found or pip executable missing at: {pip_executable}{ANSI.reset()}")
            return False

        # Try updating from PyPI
        subprocess.check_call([pip_executable, "install", "--upgrade", "SimpliPy_ML"], cwd=project_root)
        print(f"{ANSI.green()}>> Successfully updated from PyPI!{ANSI.reset()}")
        return True
    except subprocess.CalledProcessError:
        print(f"{ANSI.yellow()}>> PyPI update failed, trying GitHub...{ANSI.reset()}")
        try:
            # Try updating from GitHub
            subprocess.check_call([
                pip_executable,
                "install",
                "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
            ], cwd=project_root)
            print(f"{ANSI.green()}>> Successfully updated from GitHub!{ANSI.reset()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{ANSI.red()}>> Update failed from both sources: {e}{ANSI.reset()}")
            return False
    finally:
        os.chdir(original_cwd)


#This function here is to install dependencies
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