"""Python Library For Interacting with Chase Paymentech
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chase",
    version="2.1.2",
    author="James Maxwell",
    author_email="james@dxetech.com",
    description="Python Library for Chase Paymentech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dave2328/chase",
    packages=setuptools.find_packages(exclude=['contrib']),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='payment',
    install_requires=['requests'],
    package_data={'chase': ['*.xml']}
)
