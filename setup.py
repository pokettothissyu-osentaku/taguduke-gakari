from setuptools import setup, find_packages

with open("./requirements.txt") as file:
    requirements = file.readlines()

setup(
    name="taguduke-gakari",
    version="1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={"console_scripts": ["tagudu = tagudu:main"]},
)
