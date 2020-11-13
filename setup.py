from glob import glob
from os.path import basename, splitext

import setuptools
from pip._internal.req import parse_requirements

__version__ = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
requirements = [str(i.requirement) for i in parse_requirements('./requirements.txt', session=False)]

setuptools.setup(
    name="ejabberd_python3d",
    version=__version__,
    author="Dedaldino Antonio",
    author_email="dedaldinoantonio7@gmail.com",
    description="A library to make XML-RPC calls to ejabberd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dedaldino3D/ejabberd-python3D",
    license="MIT",
    packages=setuptools.find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: All Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.6', keywords=[
        'python', 'mix', 'django-ejabberd', 'django-auth', 'ejabberd', 'xmlrpc', 'api', 'client', 'xmpp', 'chat', 'muc'

    ],
    install_requires=requirements,
    extras_require={
    }
)
