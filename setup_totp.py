#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='totp-manager',
    version='2.0',
    description='A tool for generating time-based one-time passwords (TOTP) for services requiring multi-factor authentication (MFA), and for encrypting/managing the underlying MFA secret keys.',
    author='David M. Rosson',
    author_email='david.rosson@gmail.com',
    packages=find_packages(),
    scripts=['totp-encryptor', 'totp'],
    install_requires=['pycrypto', 'pyotp', 'pyperclip']
)
