# https://pyscard.sourceforge.io/user-guide.html
# Sample script for the reader centric approach
from smartcard.System import readers
from smartcard.util import toHexString


# find readers
r = readers()
print(r)

##### Reader centric approach

# choose specific reader with the integer found in r
# for now continue with the first found (integer 0)

# connect with the reader
connection = r[0].createConnection()
# connect with the card
connection.connect()
select = [0xA0, 0xA4, 0x00, 0x00, 0x02]
df_telecom = [0x7F, 0x10]
data, sw1, sw2 = connection.transmit(select + df_telecom)
print(sw1, sw2)
