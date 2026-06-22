from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements=f.read().splitlines()

setup(
    name="Study Buddy AI",
    version=1.0,
    author="Prince",
    packages=find_packages(),
    install_requires=requirements
)