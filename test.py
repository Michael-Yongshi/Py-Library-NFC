from source.class_nfc import NFCconnection

if __name__ == '__main__':

    nfcconnect = NFCconnection.initialize()
    print(nfcconnect.cardservice.connection.reader)
    read = nfcconnect.read_card()
    print(read)

    # pcscd 1.8.14, libnfc5 1.7.1, libccid 1.14.22