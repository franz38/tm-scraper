from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name='tmquery',
    version='0.0.3',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'requests',
        'bs4'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)