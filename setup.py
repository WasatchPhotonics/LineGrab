try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "linescan camera data visualization",
    "author": "Nathan Harrington",
    "url": "https://github.com/nharringtonwasatch/LineGrab",
    "download_url": "https://github.com/nharringtonwasatch/LineGrab",
    "author_email": "nharrington@wasatchphotonics.com.",
    "version": "1.0.0",
    "install_requires": ["numpy", "PyQt4"],
    "packages": ["linegrab"],
    "scripts": [],
    "name": "LineGrab"
}

setup(**config)
