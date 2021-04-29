import os

from dotenv import load_dotenv
from setuptools import find_packages, setup

load_dotenv()
developer = os.environ.get("DEVELOPER", "False") == "True"
install_requires = []

if developer:
    with open("requirments-dev.txt") as file:
        install_requires.extend(file.read().splitlines())

with open("requirments.txt") as file:
    install_requires.extend(file.read().splitlines())

setup(
    name="FARM-deforestation",
    version="1.0.0",
    description="Recognizing forests from aerial photos",
    author="Wail Abou",
    author_email="wail.abou@student.hu.nl",
    packages=find_packages(),
    install_requires=install_requires,
)
