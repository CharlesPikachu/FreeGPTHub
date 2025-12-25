'''
Function:
    Implementation of Setup
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu/videodl
'''
import dramamoyu as drama
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''setup'''
setup(
    name=drama.__title__,
    version=drama.__version__,
    description=drama.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=drama.__author__,
    url=drama.__url__,
    author_email=drama.__email__,
    license=drama.__license__,
    include_package_data=True,
    packages=find_packages(),
    entry_points={'console_scripts': ['dramamoyu = dramamoyu.cli:main']},
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
)