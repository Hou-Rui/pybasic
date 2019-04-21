from setuptools import setup

setup(
    name='pybasic',
    version='1.0',
    packages=['pybasic'],
    author='Hou Rui',
    author_email='13244639785@163.com',
    keywords='ply python BASIC interpreter',
    install_requires=[
        'ply>=3.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Interpreters',
    ],
)