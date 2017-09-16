from setuptools import setup

setup(
    name='djlotrek',
    version='0.0.1',
    url='https://github.com/lotrekagency/djlotrek',
    install_requires=[
        'Django >= 1.10',
        'pycrypto >= 2.6.1',
        'requests >= 2.18.4'
    ],
    description="Lotrek's beloved Django utilities library",
    long_description=open('README.md', 'r').read(),
    license="MIT",
    author="Lotrek",
    author_email="dimmitutto@lotrek.it",
    packages=['djlotrek'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)