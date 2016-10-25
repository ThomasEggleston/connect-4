from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='connect4',
    version='0.0.1',
    description='Connect 4',
    long_description=readme,
    author='Thomas Eggleston',
    author_email='thomas_eggleston@outlook.com',
    url='https://github.com/thomas_eggleston/connect4',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)