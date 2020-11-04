#! /usr/bin/env python3

from setuptools import setup, find_packages
import os 

def read_description():
    abs_path = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(abs_path) as f:
        return f.read()

setup(
    name="helloworld",
    version="0.1.2",
    packages=find_packages(),
    install_requires=['Flask~=1.1'],
    description="Hello project",
    long_description=read_description(),
    entry_points={"console_scripts": [
        'helloworld = helloworld.main:print_message',
        'web = helloworld.fl:run_server'
        ]
    }
)