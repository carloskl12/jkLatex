# instalación
import pathlib
from setuptools import setup, find_packages

from jkPyLaTeX import __version__ as VERSION

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jkPyLaTeX",
    version=VERSION,
    description="Herramienta para crear documentos LaTeX.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/carloskl12/jkPyLaTeX",
    author="Jaka",
    #author_email="office@realpython.com",
    license="GNU",
    classifiers=[
        "License :: OSI Approved :: GNU License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[] #,
#    entry_points={
#        "console_scripts": [
#            "realpython=reader.__main__:main",
#        ]
#    },
)
