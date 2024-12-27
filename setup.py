import setuptools


def def_requirements() -> list[str]:
    """
    Check PIP Requirements
    """
    pip_lines = []
    try:
        with open("requirements.txt", encoding="utf-8") as file_content:
            pip_lines = file_content.read().splitlines()
            print(f"Successfully read requirements: {pip_lines}")
    except FileNotFoundError:
        print("Error: requirements.txt not found.")
    except Exception as error:
        print(f"Unexpected error: {error}")
    return pip_lines


def def_readme() -> str:
    """
    Get Readme
    """
    readmemd = ""
    try:
        with open("README.md", encoding="utf-8") as file_content:
            readmemd = file_content.read()
    except FileNotFoundError:
        print("Error: Readme.md not found.")
    except Exception as error:
        print(f"Unexpected error: {error}")
    return readmemd


setuptools.setup(
    name="LiveChessCloud",
    version="0.0.8",
    author="eskopp",
    description="PGN Downloader for LiveChessCloud",
    long_description=def_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
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
    # install_requires=def_requirements(),
    install_requires=[
        "chess>=1.10.0",
        "colorama>=0.4.6",
        "aiohttp>=3.10.5"
    ],
    entry_points={
        "console_scripts": [
            "LiveChessCloud = LiveChessCloud.__init__:main",
        ],
    },
)
