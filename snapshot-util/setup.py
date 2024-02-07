from setuptools import setup, find_packages
setup(
    # name of package
    name="snapshot",
    # packages (directories) to be included
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snapshot = snapshot.snapshot:main",
        ],
    },
    # package dependencies
    install_requires=[
        "psutil==5.9.7",
        "argparse==1.4.0",
    ],
    version="0.1",
    author="DeBug",
    description="Example of the test application",
    license="MSU")
