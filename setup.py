#!/usr/bin/env python
from setuptools import setup, find_packages
import fastimage

setup(
    name="fastimage",
    version=fastimage.__version__,
    description="Finds the size or type of an image given its uri by fetching as little as needed",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/fastimage",
    packages=find_packages(),
    install_requires=["aiohttp>=0.22.5"],
    scripts=['bin/fastimage']
)
