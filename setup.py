from setuptools import setup, find_packages


requirements = [
    'Fabric==2.5.0',
    'invoke==1.4.0',
    'patchwork==1.0.1',
    'Jinja2==2.10.3',
    "Click==7.0",
    'python-dotenv==0.12.0',
]

VERSION = "0.14"

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
    entry_points={
        'console_scripts': [
            'carnival = carnival.cli:main',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requirements,
    test_suite="tests",
)
