from pynfc.class_nfc import NFCconnection
from pynfc.class_reference import NFCreference

if __name__ == '__main__':

    # nfcconnect = NFCconnection.initialize()
    # read = nfcconnect.read_card()
    # print(read)

    datadict = NFCreference.get_reference_material()