import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('hiermenu').__doc__.splitlines()).strip()

setup(
    name = "django-hiermenu",
    version = __import__('hiermenu').get_version().replace(' ', '-'),
    url = 'http://github.com/washingtontimes/django-hiermenu',
    author = 'Jose Soares',
    author_email = 'jsoares@washingtontimes.com',
    description = DESC,
    long_description = read_file('README'),
    packages = find_packages(),
    include_package_data = True,
    install_requires=read_file('requirements.txt'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
