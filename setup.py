from setuptools import setup

setup(name='resolver_check',
    version='0.0.1-rc1',
    description='resolver checking tool',
    url='https://{{ url }}/resolver_check.git',
    author='Richard Isberg',
    author_email='richard.isberg@gmail.com',
    license='BEER-WARE LICENSE',
    packages=['resolver_check'],
    install_requires=[
        'dnspython',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'resolver_check = resolver_check.__main__:main',
        ],
    },
    zip_safe=False)
