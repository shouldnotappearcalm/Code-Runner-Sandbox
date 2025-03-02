"""
Code Runner Python SDK安装配置
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-runner-sandbox-sdk",
    version="0.1.0",
    author="calm",
    author_email="losergzr@gmail.com",
    description="Code Runner Sandbox服务的Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shouldnotappearcalm/Code-Runner-Sandbox",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
) 