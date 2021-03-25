from setuptools import find_packages, setup

DEVELOPER = True

install_requires = []

if DEVELOPER:
    with open('requirments-dev.txt') as file:
        install_requires.extend(file.read().splitlines())

with open('requirments.txt') as file:
    install_requires.extend(file.read().splitlines())



setup(
    name='FARM-deforestation',
    version='1.0.0',
    description='Recognizing forests from aerial photos',
    author='Wail Abou',
    author_email='wail.abou@student.hu.nl',
    packages=find_packages(),
    install_requires=install_requires,
  
)