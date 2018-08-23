from setuptools import setup, find_packages

setup(
    name="snpanalyzer",
    version="0.1",

    packages=find_packages(),

    description="This package analyses SNP files.",

    license="GPLv3",

    package_data={
        "snpanalyzer.template" : ["*.tex"],
    },

    install_requires=[
        "appdirs",
        "matplotlib",
        "numpy",
        "overrides",
        "pathlib",
        "pyqt5",
        "pyvisa",
        "scikit-rf",
        "scipy",
        "singleton_decorator",
        "sympy",
        "xlsxwriter",
        "xmltodict",
    ],

    url="https://github.com/liamaltarac/SNP-Cable-Analyser",
)


