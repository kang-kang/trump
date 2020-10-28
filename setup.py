# coding=utf-8
import setuptools
from setuptools import setup
 
setup(
    name='trump',  # 应用名
    version='2.0.7',  # 版本号
    author="kangkang",
    author_email="kangkang0517@gmail.com",
    description="异步 RESTful 框架",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPL",
    url="http://git.io.gsjna.com/jna/trump",
    packages=setuptools.find_packages(),
    scripts=["scripts/trump-manager"],
    install_requires=[
        "sanic==19.6.3",
        "aioredis",
        "aiohttp",
        "sanic_session",
    ],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
)
