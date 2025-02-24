from setuptools import setup, find_packages

setup(
    name="isgoodrite",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "isgoodrite = isgoodrite.__main__:main"
        ]
    },
)