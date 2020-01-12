import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch-tree-lstm",
    version="0.1.3",
    author="Jordan Dawe",
    author_email="jordan.dawe@unbounce.com",
    description="A Tree-LSTM model package for PyTorch",
    install_requires=['numpy', 'torch'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unbounce/pytorch-tree-lstm",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
