from setuptools import setup, find_packages

setup(
    name = "django_price",
    version = "0.2.1",
    description = 'Handling price information in django',
    author = 'David Danier',
    author_email = 'david.danier@team23.de',
    url = 'https://github.com/ddanier/django_price',
    long_description=open('README.rst', 'r').read(),
    packages = [
        'django_price',
        'django_price.migrations',
    ],
    install_requires = [
        'Django >=1.4',
        'django_deferred_polymorph >=0.1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)

