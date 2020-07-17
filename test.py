from source.class_nfc import NFCconnection

if __name__ == '__main__':

    nfcconnect = NFCconnection.initialize()
    read = nfcconnect.read_card()
    print(read)

    # necessary pcscd 1.8.14, 
    # not necessary libnfc5 1.7.1, libccid 1.14.22
    # fix arc?
    # https://medium.com/@andv/how-to-fix-acr122s-and-libnfcs-unable-to-claim-usb-interface-on-kali-linux-932a34bb8e32