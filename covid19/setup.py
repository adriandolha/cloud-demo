import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eks_airflow",
    version="1.0",
    author="Adrian Dolha",
    packages=['eks_airflow'],
    author_email="adriandolha@eyahoo.com",
    description="EKS Airflow",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
