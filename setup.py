from setuptools import setup, find_packages

setup(
    name="SimpliPy_ML",
    version="0.0.1",
    description="SimpliPy_ML is a python library which makes machine-learning workflow easier.",
    author="Your Name",
    author_email="karkangelovaronapada@gmail.com",
    url="https://github.com/KarkAngelo114/SimpliPy_ML",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)