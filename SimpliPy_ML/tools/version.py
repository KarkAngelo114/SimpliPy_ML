import sys
from .._utils import _ANSI, __pkg_ver__

def checkVersion():
    required_min_version = (3, 9)
    required_max_version = (3, 10, 9)
    current_version = sys.version_info[:3]

    if required_min_version <= current_version <= required_max_version:
        print(f"\nCurrent Python version: {'.'.join(map(str, current_version))}")
    else:
        print(f"\nError: SimpliPy_ML requires Python version between {'.'.join(map(str, required_min_version))} "
              f"and {'.'.join(map(str, required_max_version))}. Please install the required version.")

def checkInfo():
    print("\nPython version info: ",sys.version_info)

def current_pkg_ver():
    local_ver = __pkg_ver__.get_local_version()

    print("\n======================================")
    print(f"{_ANSI.cyan()}SimpliPy_ML version {_ANSI.yellow()}{local_ver}{_ANSI.reset()}")
