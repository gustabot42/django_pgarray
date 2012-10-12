from distutils.core import setup


setup(
    name="django_pgarray",
    version=__import__("django_pgarray").__version__,
    author="Gustavo Diaz Jaimes",
    author_email="gustavodiazjaimes@gmail.com",
    description="array field for postgres, using csv for widget and serialization",
    long_description=open("README.rst").read(),
    url="https://github.com/gustavodiazjaimes/django_pgarray",
    packages="django_pgarray",
    install_requires = [
        "python-unicodecsv>=0.9",
    ],
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