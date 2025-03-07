from setuptools import setup, find_packages

setup(
    name="funder_communications",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "python-dotenv",
        "anthropic",
        "pandas",
        "pyyaml",
    ],
)
