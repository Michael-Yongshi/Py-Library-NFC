# Py_Library_NFC
a library to interact with nfc cards and readers from python using pyscard

## Roadmap

## Getting Started

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

## Development

### NFC
#### connecting with Pyscard
Can only be used with version 3.6.8 of python (as of moment of writing). Thus we have to switch for this application to this python version in order to use this NFC library.
Downloaded pyscard executable for windows from https://sourceforge.net/projects/pyscard/
tutorial: https://pyscard.sourceforge.io/user-guide.html
other info:
https://stackoverflow.com/questions/56423316/i-can-not-understand-my-symptoms-python-is-using-pyscard
https://github.com/GPII/linux-rfid-user-listener/blob/master/scriptor.1p
https://khanhicetea.com/post/reading-nfc-card-id-on-ubuntu/#Source-code

#### tutorial exploring apdu commands
http://tech.springcard.com/2014/reading-and-writing-data-in-a-mifare-ultralight-card-with-a-proxnroll/

#### Using ARC connect library on top of pyscard
https://github.com/StevenTso/ACS-ACR122U-NFC-Reader

https://flomio.com/forums/topic/list-of-apdu-codes/
https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses/

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#### sending commands with libnfc

#### rfidiot.py
https://github.com/AdamLaurie/RFIDIOt/blob/master/rfidiot/RFIDIOt.py

#### connecting with nfcpy, uses libnfc
https://nfcpy.readthedocs.io/en/latest/topics/get-started.html

download libusb
https://libusb.info/

```
pip3 install --user nfcpy
```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#### encoding with ndeflib
encoding and decoding messages from NDEF format (nfc data exchange format)
```
pip3 install --user ndeflib
```

https://pypi.org/project/ndeflib/
https://ndeflib.readthedocs.io/en/latest/ndef.html

tabs:
https://github.com/Microsoft/Windows-universal-samples/tree/master/Samples/Nfc
https://stackoverflow.com/questions/56288102/which-apdu-to-use-to-read-write-records-on-mifare-ultralight-nfc-tag
https://gist.github.com/im-infamou5/4681713
http://nfc-tools.org/index.php/Libnfc:APDU_example
https://stackoverflow.com/questions/47820902/cannot-send-large-apdu-commands-with-libnfc-using-nfc-initiator-transceive-bytes
https://stackoverflow.com/search?q=nfc+read+command+apdu
https://stackoverflow.com/questions/34869625/how-to-read-or-write-smart-card
https://stackoverflow.com/questions/56261178/cant-read-card-with-nfc-rfid-reader-through-python

## Running the tests



### Break down into end to end tests



### And coding style tests



## Deployment



## Built With



## Contributing



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
