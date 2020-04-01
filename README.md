# Python_NFC_Lib
a library to interact with nfc cards and readers from python using pyscard

## Roadmap

## Getting Started

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

#### Using ARC connect library on top of pyscard
https://github.com/StevenTso/ACS-ACR122U-NFC-Reader

https://flomio.com/forums/topic/list-of-apdu-codes/
https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses/


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



## Acknowledgments
