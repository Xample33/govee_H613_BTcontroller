from os import path

from setuptools import setup


def read(fname):
    return open(path.join(path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name="govee_H613_BTcontroller",
    version="1.0.2",
    packages=["govee_H613_BTcontroller"],
    author="Xample33",
    maintainer="Xample33",
    license="MIT",
    url="https://github.com/Xample33/govee_H613_BTcontroller",
    description="A Python library for controlling Govee H613 Bluetooth LED strip.",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        "bleak",
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords="govee bluetooth led strip H613",
)
