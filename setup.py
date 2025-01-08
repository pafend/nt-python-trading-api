from setuptools import setup, find_packages

setup(
    name="nt_trading_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "watchdog>=2.1.0",  # For monitoring file changes
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    author="Pascal Fend",
    author_email="pascal@pascalfend.de",
    description="A Python API for NinjaTrader's automated trading interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pafend/nt-python-trading-api",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
) 