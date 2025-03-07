from setuptools import setup, find_packages
from os import path

top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

with open(path.join(top_level_directory, 'requirements.txt')) as file:
    required = file.read().splitlines()

setup(
    name="updownapp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "updownapp=updownapp.app:main",
        ],
    },
    description="A minimal HTTP file transfer server",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Andrea Esuli",
    author_email="andrea@esuli.it",
    license='BSD',
    url="https://github.com/aesuli/updownapp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    license_files = ('LICENSE',),
    python_requires='>=3.8',
    project_urls={
        'Bug Reports': 'https://github.com/aesuli/updownapp/issues',
        'Source': 'https://github.com/aesuli/updownapp/',
    },
)