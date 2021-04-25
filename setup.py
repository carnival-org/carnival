from os import path

from setuptools import find_packages, setup

requirements = [
    'Fabric==2.5.0',
    'invoke==1.4.0',
    'patchwork==1.0.1',
    'Jinja2>=2.11.3',
    "Click==7.0",
    'python-dotenv==0.12.0',
]

VERSION = "1.3"

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='carnival',
    version=VERSION,
    include_package_data=True,
    packages=find_packages(),
    url='https://github.com/carnival-org/carnival',
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='Fabric-based software provisioning tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'carnival = carnival.cli:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',

        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=requirements,
    test_suite="tests",
)
