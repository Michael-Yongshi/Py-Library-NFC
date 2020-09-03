from pynfc.class_nfc import NFCconnection

if __name__ == '__main__':

    nfcconnect = NFCconnection.initialize()
    read = nfcconnect.read_card()
    print(read)
