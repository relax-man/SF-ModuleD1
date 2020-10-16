import setuptools  

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trello-client-relax-man",
    version="0.0.1",
    author="Michael",
    author_email="kobtsev.x@gmail.com",
    description="Small python program that implements the features of trello",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/relax-man/SF-ModuleD1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)  
