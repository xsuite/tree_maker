"""
setup.py for datascout.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, find_packages


HERE = Path(__file__).parent.absolute()
with (HERE / "README.md").open("rt") as fh:
    LONG_DESCRIPTION = fh.read().strip()


REQUIREMENTS: dict = {
    "core": ["numpy", "scipy", "pandas", "pyarrow", "awkward", "datetime", "pathlib"],
    "test": [
        "pytest",
    ],
    "dev": [
        # 'requirement-for-development-purposes-only',
    ],
    "doc": [
        "sphinx",
        "acc-py-sphinx",
    ],
}


setup(
    name="datascout",
    version="0.0.2",
    author="Davide Gamba",
    author_email="davide.gamba@cern.ch",
    description="Sweet functions for dict from/to pandas, awkward, parquet data conversion.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://acc-py.web.cern.ch/gitlab/abpcomputing/sandbox/tree_maker/docs/stable/",
    packages=find_packages(),
    python_requires="~=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS["core"],
    extras_require={
        **REQUIREMENTS,
        # The 'dev' extra is the union of 'test' and 'doc', with an option
        # to have explicit development dependencies listed.
        "dev": [
            req
            for extra in ["dev", "test", "doc"]
            for req in REQUIREMENTS.get(extra, [])
        ],
        # The 'all' extra is the union of all requirements.
        "all": [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
