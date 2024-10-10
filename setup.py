from setuptools import setup, find_packages

setup(
    name="morning_greetings",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Any dependencies you have
    entry_points={
        'console_scripts': [
            'morning_greetings = morning_greetings.main:main',
        ],
    }
)