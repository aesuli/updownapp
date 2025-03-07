from setuptools import setup, find_packages

setup(
    name="updownapp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cherrypy",
    ],
    entry_points={
        "console_scripts": [
            "updownapp=updownapp.app:main",
        ],
    },
    description="A minimal HTTP file transfer server",
    author="Andrea Esuli",
    author_email="andrea@esuli.it",
    url="https://github.com/aesuli/updownapp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)