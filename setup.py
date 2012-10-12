from distutils.core import setup
from django_pgarray import __version__


setup(
    name="django_pgarray",
    version=__version__,
    author="Gustavo Diaz Jaimes",
    author_email="gustavodiazjaimes@gmail.com",
    description="array field for postgres, using csv for widget and serialization",
    long_description=open("README.rst").read(),
    url="https://github.com/gustavodiazjaimes/django_pgarray",
    packages=["django_pgarray",],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
)