"""
Maze Solver - A clean, offline-capable maze solving application
"""
from setuptools import setup, find_packages

setup(
    name="maze-solver",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.1",
        "numpy>=1.21.2",
    ],
    author="Your Name",
    description="A clean maze solving application with multiple algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)