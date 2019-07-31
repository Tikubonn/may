
from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="may",
    version="1.0.0",
    description="this is a FTP wrapper library, like as built in file system library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tikubonn",
    author_email="https://twitter.com/tikubonn",
    url="https://github.com/tikubonn/may",
    license="MIT",
    packages=find_packages(exclude=("test",)),
    install_requires=[],
                extras_require={
        "test": [
            "pyftpdlib",
        ],
    },
    dependency_links=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'License :: OSI Approved :: MIT License',
    ],
    test_suite='test'
)
