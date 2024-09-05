import setuptools


def def_requirements() -> str:
    """
    Check PIP Requirements
    """
    pip_lines = ""
    try:
        with open("requirements.txt", encoding="utf-8") as file_content:
            pip_lines = file_content.read().splitlines()
            print(f"{pip_lines}")
    except Exception as error:
        print(f"Execpiton: {error}")
    return pip_lines 


def def_readme() -> str:
    """
    Get Readme
    """
    readmemd = ""
    try:
        with open("Readme.md", encoding="utf-8") as file_content:
            readmemd = file_content.read()
    except Exception as error:
        print(f"Execpiton: {error}")
    return readmemd


setuptools.setup(
    name="LiveChessCloud",
    version="0.0.7",
    author="eskopp",
    description="PGN Downloader for LiveChessCloud",
    long_description=def_readme(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/eskopp/LiveChessCloud",
    packages=["LiveChessCloud"],
    package_data={"LiveChessCloud": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=def_requirements(),
    entry_points={
        "console_scripts": [
            "LiveChessCloud = LiveChessCloud.__init__:main",
        ],
    },
)
