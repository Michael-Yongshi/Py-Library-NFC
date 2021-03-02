import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yongshi-pynfc",
    version="0.4.3",
    author="Michael-Yongshi",
    author_email="4registration@outlook.com",
    description="A nfc library for python based solely on pyscard to communicate with the nfc card and ndeflib to arrange encoding and decoding of messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michael-Yongshi/Py-Library-NFC",
    packages=setuptools.find_packages(),
    data_files=[
        (os.path.join('pynfc'), [
            os.path.join('pynfc', 'nfc_communication.json'),
            ])
        ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)