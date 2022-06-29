import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lorem_ipsum_auth",
    version="1.0",
    author="Adrian Dolha",
    packages=[],
    author_email="adriandolha@eyahoo.com",
    description="Lorem Ipsum Demo App Auth",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
