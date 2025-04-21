import sys

if not any("__main__" in module for module in sys.modules):
    raise ImportError("The '_utils' module is for internal use only and cannot be imported directly.")