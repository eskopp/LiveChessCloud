import setuptools


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
    version="0.1.0",
    author="eskopp",
    description="PGN Downloader for LiveChessCloud",
    long_description=def_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/eskopp/LiveChessCloud",
    packages=setuptools.find_packages(),
    package_data={"LiveChessCloud": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "colorama==0.4.6",
        "click==8.2.1",
        "requests==2.32.3",
        "asyncio==3.4.3",
        "chess==1.11.2",
        "pytest==8.3.5",
        "aiohttp==3.11.13",

    ],
    entry_points={
        'console_scripts': [
            'livechesscloud=LiveChessCloud.__init__:main',
            'LiveChessCloud=LiveChessCloud.__init__:main',
            'LIVECHESSCLOUD=LiveChessCloud.__init__:main'
        ],
    },
)
