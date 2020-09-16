from pynfc.class_nfc import NFCconnection

if __name__ == '__main__':

    nfcconnect = NFCconnection.initialize()
    read = nfcconnect.read_card()
    print(read)

    plaindata = "string"
    nfcconnect.write_card(data=plaindata)

    integerdata = 582
    nfcconnect.write_card(data=integerdata)

    bytedata = b'c\xdevQL\xcc\xf5\xad%\x11\xb1\xda\x10\x14\xdc\xf0\x0f\x9d\xcc3N\xa9\xa5i\xae\x0e\xceHv\x81KzV\xe1y0\xd02\x95\xb6\xec\xe5\x15\x84\xd0\xb3\xb4M\xe8\xda\x96\xee  )\x08SF\x82\xec\xf1i\x14X\x9fP\x15\xd5\xae\xed8\xd7 =\xa5T\x89\x82X\xe5'
    nfcconnect.write_card(data=bytedata)