"""
Setup file for the project
"""

from setuptools import setup


setup(
    name='foostats',
    package=['foostats'],
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
