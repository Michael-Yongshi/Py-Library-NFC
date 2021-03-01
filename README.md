# Py_Library_NFC
a library to interact with nfc cards and readers from python using pyscard and ndeflib

## Roadmap

## Getting Started
### pyscard
for windows:
```
pip install pyscard
```

for ubuntu:
```
sudo apt install swig
sudo apt install -y python3-pyscard
sudo apt install pcscd # needed to scan for readers on ubuntu

# if you get errors (ARC nfc reader has this with ubuntu)
sudo vim /etc/modprobe.d/blacklist-libnfc.conf
# Add this line: blacklist pn533_usb
# Reboot
```

### ndef library
```
pip install ndeflib
```

## Development

### NFC
#### connecting with Pyscard
Should be usable with python version 3.3 or higher, but Tested on version 3.6.8.

### other info sources used for development of this library
#### pyscard
pyscard tutorial: https://pyscard.sourceforge.io/user-guide.html

#### Using ARC connect library on top of pyscard
https://github.com/StevenTso/ACS-ACR122U-NFC-Reader

#### libusb
usb library for linux

download libusb
https://libusb.info/

#### encoding with ndeflib
encoding and decoding messages from NDEF format (nfc data exchange format)

https://pypi.org/project/ndeflib/
https://ndeflib.readthedocs.io/en/latest/ndef.html

## Running the tests
After cloning the repo and downloading the dependencies, run the following script:
```
python3 test_class_nfc.py
```

To test completely it expects a valid ARC nfc reader and a presented nfc card

### Break down into end to end tests



### And coding style tests



## Deployment



## Built With



## Contributing

### contributors
JJCC
https://github.com/jjcc
Fixes for Android app compatibility

## Versioning



## Authors

* **Michael-Yongshi** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Licensed under a MIT Licence, see LICENSE file for details.

Copyright © 2020 WAM-Desktop contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments
