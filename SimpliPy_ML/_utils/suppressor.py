import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
import sys

if not any("__main__" in module for module in sys.modules):
    raise ImportError("This module is for internal use only and cannot be imported directly.")

def suppress():
    warnings.filterwarnings('ignore')