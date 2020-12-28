import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kolonial",
    version="0.1.0",
    author="Fredrik Haarstad",
    author_email="codemonkey@zomg.no",
    description="Python wrapper for the Kolonial.no API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frefrik/python-kolonial",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
