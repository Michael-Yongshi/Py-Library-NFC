import ndef

from pynfc.pyscard_ndeflib import (
    NFCconnection,
    decode_message,
    encode_message_text,
)

# decode hexstring payload to ndef text message
array_of_strings = decode_message(b'\x91\x01\x08T\x02enHelloQ\x01\x08T\x02enWorld')
print("")
payload_encoded = encode_message_text(["Hello", "World"])
print("")

nfcconnect = NFCconnection.initialize()
nfcconnect.wipe_card()
nfcconnect.write_card(data=payload_encoded)
print("")

payload_received = nfcconnect.read_card()
print("")

payload_decoded = decode_message(payload_received)
print(payload_decoded)