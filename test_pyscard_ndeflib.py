import ndef

from pynfc.pyscard_ndeflib import (
    NFCconnection,
    decode_message,
    encode_message_text,
)

# decode hexstring payload to ndef text message
array_of_strings = decode_message(b'\x91\x01\x08T\x02enHelloQ\x01\x08T\x02enWorld')
print("")
payload = encode_message_text(["Hello", "World"])
print("")

nfcconnect = NFCconnection.initialize()
nfcconnect.wipe_card()
nfcconnect.write_card(data=payload)
print("")

received_payload = nfcconnect.read_card()
print("")

array_of_received = decode_message(received_payload)