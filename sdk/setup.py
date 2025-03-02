"""
Code Runner Python SDK安装配置
"""
from setuptools import setup, find_packages
import os

with open("code_runner_sdk/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 确保包含所有Python模块
packages = find_packages(include=['code_runner_sdk', 'code_runner_sdk.*'])

setup(
    name="code-runner-sdk",
    version="0.1.1",
    author="calm",
    author_email="losergzr@gmail.com",
    description="Code Runner Sandbox服务的Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shouldnotappearcalm/Code-Runner-Sandbox",
    packages=packages,
    package_data={
        'code_runner_sdk': ['**/*.py'],  # 包含所有Python文件
    },
    include_package_data=True,
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