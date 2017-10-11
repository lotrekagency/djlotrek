from setuptools import setup, find_packages

setup(
    name='djlotrek',
    version='0.0.4',
    url='https://github.com/lotrekagency/djlotrek',
    install_requires=[
        'Django >= 1.10',
        'pycrypto >= 2.6.1',
        'requests >= 2.18.4'
    ],
    description="Lotrek's beloved Django utilities library",
    long_description=open('README.rst', 'r').read(),
    license="MIT",
    author="Lotrek",
    author_email="dimmitutto@lotrek.it",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)