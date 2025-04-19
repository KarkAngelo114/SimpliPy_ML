import subprocess
import sys
from ..__utils__ import ANSI

def self_update():
    """
    Calling this function will update the SimpliPy_ML module.
    """
    try:
        print("\n=================================")
        print(f"{ANSI.cyan()}>> Updating {ANSI.yellow()}SimpliPy_ML{ANSI.reset()}\n")
        
        # Corrected pip command for updating
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "SimpliPy_ML"])
        print(f"{ANSI.green()}>> Successfully updated SimpliPy_ML{ANSI.reset()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{ANSI.red()}>> Failed to update SimpliPy_ML: {e}{ANSI.reset()}")
        return False

def package_install(package_name):
    """
    Installs the required libraries for SimpliPy_ML.
    If package_name is '*', installs all dependencies.
    """

    dependencies = ["tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx"]

    try:
        if package_name == "*":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing all required libraries...{ANSI.reset()}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx"
            ])

        elif package_name.lower() == "tensorflow":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "keras":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "numpy":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        
        elif package_name.lower() == "numpy":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "pillow":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "scikit-learn":
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "keras2onnx":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "onnxruntime":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name.lower() == "onnx":
            print("\n=================================")
            print(f"{ANSI.cyan()}>> Installing {package_name}...{ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

        elif package_name == "":
            print("\n=================================")
            print(f"{ANSI.red()}>> Specify the package name {ANSI.reset()}")
        
        elif package_name not in dependencies:
            print("\n=================================")
            print(f"{ANSI.red()}>> {package_name} is not a dependency of SimpliPy_ML {ANSI.reset()}")
        

        if package_name != "" and package_name in dependencies:
            print(f"{ANSI.green()}>> Successfully installed {package_name}{ANSI.reset()}")
            return True

        elif package_name == "*":
             print(f"{ANSI.green()}>> Successfully installed all libraries{ANSI.reset()}")
        

        
       
    except subprocess.CalledProcessError as e:
        print(f"{ANSI.red()}>> Failed to install {package_name}: {e}{ANSI.reset()}")
        return False