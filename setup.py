from setuptools import setup, find_packages, Extension
from yagimaid import __version__, __author__, __email__


with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

with open("README.md", encoding='utf-8') as file:
    long_description = file.read()

setup (
    name = 'yagimaid',
    version = __version__,
    keywords = ['yagimaid', 'raito', 'raitonoberu', 'light novel downloader', 'novel'],
    description = 'light novel downloader',
    author = __author__,
    author_email = __email__,
    license = 'MIT',
    url = 'https://github.com/arasHi87/RaitoNoberu',
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages = find_packages(),
    include_package_data = True,
    install_requires = requirements,
    entry_points={
        'console_scripts': [
            'yagimaid = yagimaid.main:main',
        ]
    }
)