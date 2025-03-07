from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="updownapp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['CherryPy==18.10.0'],
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
    license_files = [],
    python_requires='>=3.8',
    project_urls={
        'Bug Reports': 'https://github.com/aesuli/updownapp/issues',
        'Source': 'https://github.com/aesuli/updownapp/',
    },
)