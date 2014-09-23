#! coding:utf-8

from setuptools import setup


setup(
    name='fasttrace',
    version='0.1',
    description='Fast tracing tool',
    author='Rustem Muslimov',
    url='https://github.com/rmuslimov/fasttrace',
    packages=[
        'fasttrace',
    ],
    install_requires=[
        'pika>=0.9.14',
        'pylibmc>=1.3.0',
        'ujson>=1.33',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.3.1',
    ],
)
