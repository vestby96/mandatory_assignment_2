from setuptools import setup, find_packages

setup(
    name="morning_greetings",  # The name of your package
    version="0.1",
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[],  # Add any dependencies here, e.g. ['schedule', 'requests']
    entry_points={
        'console_scripts': [
            'morning_greetings = morning_greetings.main:main',  # The command 'morning_greetings' will call main()
        ],
    },
    author="Your Name",
    author_email="your_email@example.com",
    description="A package that sends Good Morning messages to contacts",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)