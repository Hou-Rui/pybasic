from setuptools import setup

setup(
    name='ply-pybasic',
    version='1.1',
    packages=['pybasic'],
    author='Hou Rui, Peter Yang',
    author_email='13244639785@163.com,turmary@126.com',
    keywords='ply python BASIC interpreter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Hou-Rui/pybasic',
    install_requires=[
        'ply>=3.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Interpreters',
    ],
)