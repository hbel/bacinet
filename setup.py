import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bacinet",
    version="0.0.4",
    author="Hendrik Belitz",
    author_email="hendrik@hendrikbelitz.de",
    description="Setting up security-relevant response headers in FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hbel/bacinet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'fastapi'
    ],
    keywords='FastAPI headers http',
    project_urls={
        'Homepage': 'https://github.com/hbel/bacinet',
    },
)
