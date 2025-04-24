from .._utils import _ANSI
import sys
import subprocess

def forceFix_dependencies(package_name):
    """
        Calling this function will fix dependencies/libraries that SimpliPy_ML is relying on. 
        It will simply force reinstall all packages to ensure that they will return to their state.
        Please note that using this function will force reinstall the dependencies and will take time to reinstall them.

        Parameters:

        "*": This will reinstall all dependencies

        package_name (str): specify thr package name that SimpliPy_ML depends on to fix. It will be force reinstall, ensuring that will go back to it's normal state
    """

    dependencies = ["tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn", 'tabulate']

    try:
        if package_name == "*":
            print("\n=================================")
            print(f"{_ANSI.cyan()}>> Fixing dependencies. This might take a while{_ANSI.reset()}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--force-reinstall",
                "tensorflow", "keras", "numpy", "matplotlib", 
                "pillow", "scikit-learn", "keras2onnx", 
                "onnxruntime", "onnx", "seaborn", 'tabulate'
            ])

        elif package_name.lower() in dependencies:
            print("\n=================================")
            print(f"{_ANSI.cyan()}>> Reinstalling {package_name}...{_ANSI.reset()}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", package_name])
        

        if package_name != "" and package_name in dependencies:
            print(f"{_ANSI.green()}>> Successfully installed {package_name}{_ANSI.reset()}")
            return True

        elif package_name == "*":
            print(f"{_ANSI.green()}>> Successfully Reinstalled all libraries{_ANSI.reset()}")
            return True

        elif package_name != "" and package_name not in dependencies:
            print(f"{_ANSI.red()}>> {package_name} is not in it's dependencies.{_ANSI.reset()}")
            return False

       
    except subprocess.CalledProcessError as e:
        print(f"{_ANSI.red()}>> Failed to Reinstall {package_name}: {e}{_ANSI.reset()}")
        return False