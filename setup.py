from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    import warnings
    warnings.warn('warning: pypandoc module not found, could not convert Markdown to RST')
    read_md = lambda f: open(f, 'r').read()



setup(
    name='logstats',
    version='0.1.0',

    description='A module to collect and display stats for long running processes',
    long_description=read_md('README.md'),

    url='https://github.com/vrde/logstats',

    author='Alberto Granzotto',
    author_email='agranzot@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],

    packages=['logstats']
)
