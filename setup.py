from setuptools import setup, find_packages

setup(
    name="cyber-ragnarok",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "groq",
    ],
)