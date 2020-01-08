from setuptools import setup, find_packages

version = '0.1'

requirements = [
    'Fabric==2.5.0',
]


setup(
    name='carnival',
    version=version,
    packages=find_packages(where='carnival'),
    url='https://github.com/a1fred/carnival',
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='Fabric-based software provisioning tool',
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
