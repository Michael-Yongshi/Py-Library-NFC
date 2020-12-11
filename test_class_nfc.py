import ndef

from pynfc.pyscard_ndeflib import (
    NFCconnection,
    decode_message_text,
    encode_message_text,
)

# decode hexstring payload to ndef text message
decode_message_text(b'\x91\x01\x08T\x02enHelloQ\x01\x08T\x02enWorld')
print("")

# encode message(s) to a hexstring payload
payload_encoded = encode_message_text(["Hello", "World"])
print("")

# write the message to the card
nfcconnect = NFCconnection.initialize()
nfcconnect.wipe_card()
nfcconnect.write_card(data=payload_encoded)
print("")

# read the card
payload_received = nfcconnect.read_card()
print("")

# decode the received payload
payload_decoded = decode_message_text(payload_received)
print(payload_decoded)