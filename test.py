from pynfc.class_nfc import NFCconnection

if __name__ == '__main__':

    nfcconnect = NFCconnection.initialize()
    read = nfcconnect.read_card()
    print(read)

    plaindata = "string"
    nfcconnect.write_card(data=plaindata)

    integerdata = 582
    nfcconnect.write_card(data=integerdata)

    bytedata = b'\xee\xa42}\x01Ja\x9f~\xf4W\xb0g\x88\xb0\xcb\x8d\x84A,\x1e\xa0g-TX\xf0\xf0I\x96\xda\x07f,P%\xb1\x918\xfdu\xbeH\xfa\xd0\x85G\x17F\x9e\x81\xcbh\xda[;\xc9\x06\x19\xa7\xaf\x94\xba\x8e<\xd2E\xd2\x89\xca\x0fu\xc5Pj\x87\xcd\x84!\xc3'
    nfcconnect.write_card(data=bytedata)