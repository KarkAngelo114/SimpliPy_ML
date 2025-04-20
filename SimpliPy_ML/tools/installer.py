import os
import subprocess
import sys
from ..__utils__ import ANSI
import venv

def self_update():
    """
    Calling this function will update SimpliPy_ML to newer versions available.
    Ensures pip is executed within the project's virtual environment.
    """

    print("\n=================================")
    print(f"{ANSI.cyan()}>> Updating {ANSI.yellow()}SimpliPy_ML{ANSI.reset()}\n")

    # Save the current working directory (though we might not need to change it)
    original_cwd = os.getcwd()

    try:
        # Determine the path to the virtual environment directory
        project_root = os.path.dirname(os.path.abspath(sys.argv[0]))
        venv_path = os.path.join(project_root, ".venv")

        # Construct the path to the pip executable within the virtual environment
        pip_executable = os.path.join(venv_path, "bin", "pip")  # For Linux/macOS
        if sys.platform == "win32":
            pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")

        if not os.path.exists(pip_executable):
            print(f"{ANSI.yellow()}>> Virtual environment not found or pip executable missing at: {pip_executable}{ANSI.reset()}")
            return False

        # Try updating from PyPI
        subprocess.check_call([pip_executable, "install", "--upgrade", "SimpliPy_ML"])
        print(f"{ANSI.green()}>> Successfully updated from PyPI!{ANSI.reset()}")
        return True
    except subprocess.CalledProcessError:
        print(f"{ANSI.yellow()}>> PyPI update failed, trying GitHub...{ANSI.reset()}")
        try:
            # Try updating from GitHub
            subprocess.check_call([
                pip_executable,
                "install",
                "--upgrade",
                "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
            ])
            print(f"{ANSI.green()}>> Successfully updated from GitHub!{ANSI.reset()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{ANSI.red()}>> Update failed from both sources: {e}{ANSI.reset()}")
            return False
    finally:
        # Restore the original working directory (optional, as we might not have changed it)
        os.chdir(original_cwd)

# def self_update():
#     """
#         Calling this function will update SimpliPy_ML to newer versions available
#     """

#     print("\n=================================")
#     print(f"{ANSI.cyan()}>> Updating {ANSI.yellow()}SimpliPy_ML{ANSI.reset()}\n")

#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "SimpliPy_ML"])
#         print(f"{ANSI.green()}>> Successfully updated from PyPI!{ANSI.reset()}")
#         return True
#     except subprocess.CalledProcessError:
#         print(f"{ANSI.yellow()}>> PyPI update failed, trying GitHub...{ANSI.reset()}")
#         try:
#             subprocess.check_call([
#                 sys.executable,
#                 "-m", "pip",
#                 "install",
#                 "--upgrade",
#                 "git+https://github.com/KarkAngelo114/SimpliPy_ML.git"
#             ])
#             print(f"{ANSI.green()}>> Successfully updated from GitHub!{ANSI.reset()}")
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"{ANSI.red()}>> Update failed from both sources: {e}{ANSI.reset()}")
#             return False



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