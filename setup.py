#!/usr/bin/env python
from setuptools import setup, find_packages
from fastimage import version

setup(
    name="fastimage",
    version=version,
    description="Finds the size or type of an image given its uri by fetching as little as needed",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/fastimage",
    packages=find_packages(),
    requires=["twisted.internet", "treq"],
    install_requires=['twisted>=12.0', "treq>=0.2.1"]
)
