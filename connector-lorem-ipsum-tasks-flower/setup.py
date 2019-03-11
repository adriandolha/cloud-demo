import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connector_lorem_ipsum",
    version="1.0",
    author="Adrian Dolha",
    packages=['connector_lorem_ipsum'],
    author_email="adriandolha@eyahoo.com",
    description="Connector Lorem Ipsum",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
