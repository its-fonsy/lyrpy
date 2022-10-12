
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lyrpy",
    version="0.0.1",
    author="Marco Fontana",
    author_email="ciabadiale@gmail.com",
    description="Terminal application to display lyrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    url="https://github.com/its-fonsy/lyrpy",
    packages=setuptools.find_namespace_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux" ],
    python_requires=">=3.8",
    install_requires=[ "python-mpd2", "requests", "bs4", "pycmus" ],
    entry_points={ "console_scripts": [ "lyrpy = lyrpy.lyrpy:main" ]}
)
