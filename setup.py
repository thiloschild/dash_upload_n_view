# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(  name='dash_upload_n_view',
        packages=find_packages(),
        version='0.0.1',
        description='Description.',
        long_description='Long description.',
        author='Thilo Schild',
        author_email='t.shild@uni-mainz.de',
        url='https://github.com/MatteoLacki/dash_upload_n_view.git',
        keywords=['Great module', 'Devel Inside'],
        classifiers=['Development Status :: 1 - Planning',
                     'License :: OSI Approved :: BSD License',
                     'Intended Audience :: Science/Research',
                     'Topic :: Scientific/Engineering :: Chemistry',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7'],
        install_requires=['pandas', 'dash', 'dash-bootstrap-components','toml'],
        scripts = ['bin/test_dash_upload_n_view.py']
)
