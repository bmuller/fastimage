#!/usr/bin/env python
from setuptools import setup, find_packages
import os.path

with open(os.path.join(os.path.dirname(__file__), "fastimage", "_version")) as ver:
    version = ver.readline().strip()

setup(
    name="fastimage",
    version=version,
    package_data={"fastimage": ["_version"]},
    description="Finds the size or type of an image given its uri by fetching as little as needed",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/fastimage",
    packages=find_packages(),
    requires=["twisted.internet", "treq"],
    install_requires=['twisted>=12.0', "treq>=0.2.1"]
)
