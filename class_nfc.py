# https://pyscard.sourceforge.io/user-guide.html
# Sample script for the card centric approach
from __future__ import print_function
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.util import toHexString, toBytes
from smartcard.System import readers

class NFCmethods(object):
    def __init__(self):
        super().__init__()


    @staticmethod
    def parse_string_from_codes(datacodes):
        
        datahexstring = ""

        for i in datacodes:
            i_hexstring = format(i, '#04x')[2:]
            i_upper = i_hexstring.upper()
            datahexstring += i_upper

        return datahexstring

    @staticmethod
    def stringParser(data_in):
        """--------------String Parser--------------"""
        # #([85, 203, 230, 191], 144, 0) -> [85, 203, 230, 191]
        # if isinstance(data_in, tuple):
        #     temp = data_in[0]
        #     code = data_in[1]
        # #[85, 203, 230, 191] -> [85, 203, 230, 191]
        # else:
        #     temp = data_in
        #     code = 0

        temp = data_in

        # print(f"data_in = {data_in}")
        data_out = ""

        #[85, 203, 230, 191] -> bfe6cb55 (int to hex reversed)
        for val in reversed(temp): # 85
            # print(f"val = {val}")
            formatval = format(val, '#04x')[2:] # bf
            # print(f"formatted = {formatval}")
            data_out += formatval # bfe6cb55
            # print(f"data_out = {data_out}")

        data_out = data_out.upper() #bfe6cb55 -> BFE6CB55
        # print(f"data_out_upper = {data_out}")

        return data_out

    @staticmethod
    def get_card_block_length(atr):
        # the block length
        length = "Unknown"

        # 
        atrhex = toHexString(atr)
        length_string = atrhex[18:20]
        # "OC" apparantly means 12 bytes of config data
        # print(f"length_string: {length_string}")
     
        if length == "Unknown":
            length += f" - length code: {length_string}"

        return length

    @staticmethod
    def get_card_rid(atr):
        # also known as RID or Registered App Provider Identifier
        rid = "Unknown"

        rids = {
            "A0 00 00 03 06": "PC/SC Workgroup",
        }

        # 9th position, pythons first position is 0, so 9-1=8
        atrhex = toHexString(atr)
        rid_string = atrhex[21:35]

        # print(f"rid_string: {rid_string}")

        for key in rids:
            if key == rid_string:
                rid = f"{rids[key]} (code: {key})"
                break
        
        if rid == "Unknown":
            rid += f" - RID code: {rid_string}"

        return rid

    @staticmethod
    def get_card_standard(atr):
        # the iso standard that is followed
        standard = "Unknown"

        standards = {
            "03": "ISO14443A, Part3", # standard format
        }

        # 
        atrhex = toHexString(atr)
        standard_string = atrhex[36:38]

        # print(f"standard_string: {standard_string}")

        for key in standards:
            if key == standard_string:
                standard = f"{standards[key]} (code: {key})"
                break
        
        if standard == "Unknown":
            standard += f" - standard code: {standard_string}"

        return standard

    @staticmethod
    def get_card_type(atr):

        card_type = "Unknown"

        card_types = {
            "00 01": "Mifare 1K",
            "00 02": "Mifare 4k",
            "00 03": "Mifare Ultralight",
            "00 26": "Mifare Mini",
            "F0 04": "Topaz and Jewel",
            "F0 11": "Felica 212k",
            "F0 12": "Felica 424k",
        }

        atrhex = toHexString(atr)
        card_type_string = atrhex[39:44]

        for key in card_types:
            if key == card_type_string:
                card_type = f"{card_types[key]} (code: {key})"
                break
        
        if card_type == "Unknown":
            card_type += f" - card name code: {card_type_string}"

        return card_type

    @staticmethod
    def get_card_rfu(atr):
        # something to do with clock frequencies, are often left at 0 to set default setting.
        rfu = "Unknown"

        rfus = {
            "00 00 00 00": "Default setting",
        }

        atrhex = toHexString(atr)
        rfu_string = atrhex[45:56]

        for key in rfus:
            if key == rfu_string:
                rfu = f"{rfus[key]} (code: {key})"
                break
        
        if rfu == "Unknown":
            rfu += f" - card name code: {rfu_string}"

        return rfu

class NFCconnection(object):
    def __init__(self, cardservice):
        super().__init__()
        self.cardservice = cardservice

    @staticmethod
    def initialize_any():

        cardtype = AnyCardType() # for accepting any type of card
        cardrequest = CardRequest( timeout=1, cardType=cardtype )

        print("Waiting for card")
        cardservice = cardrequest.waitforcard()
        print("Card found")
        # connecting to card
        cardservice.connection.connect()
        print("Connection established")
        print("")

        reader = cardservice.connection.getReader()
        print(f"connected to reader: {reader}")
        atr = cardservice.connection.getATR()
        print(f"connected to card (in bytes): {str(atr)}")
        atrhex = toHexString(atr)
        print(f"connected to card (in hex): {str(atrhex)}")
        print("")

        # get some info out of ATR:
        length = NFCmethods.get_card_block_length(atr)
        print(f"byte 7 // config data length: {length}")
        rid = NFCmethods.get_card_rid(atr)
        print(f"bytes 8 - 12 // rid: {rid}")
        standard = NFCmethods.get_card_standard(atr)
        print(f"byte 13 // standard: {standard}")
        card_type = NFCmethods.get_card_type(atr)
        print(f"bytes 14 - 15 // cardtype: {card_type}")
        rfu = NFCmethods.get_card_rfu(atr)
        print(f"bytes 16 - 19 // rfu: {rfu}")

        return NFCconnection(
            cardservice = cardservice,
        )

    @staticmethod
    def initialize_specific(atr, atrhex):

        # data for the card based on the received ATR (using nfc tools)
        mycardatr = atr
        print(f"mycardatr: {mycardatr}")
        mycardhex = toHexString(atrhex)
        print(f"mycardhex: {mycardhex}")
        mycardbytes = toBytes(mycardhex)
        print(f"mycardbytes: {mycardbytes}")

        # Sample script for the smartcard.ATR utility class.
        atr = ATR(atrhex)

        print(atr)
        print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
        print('checksum: ', "0x%X" % atr.getChecksum())
        print('checksum OK: ', atr.checksumOK)
        print('T0  supported: ', atr.isT0Supported())
        print('T1  supported: ', atr.isT1Supported())
        print('T15 supported: ', atr.isT15Supported())

        cardtype = AnyCardType() # for accepting any type of card
        # cardtype = ATRCardType(mycardbytes) # for accepting a specific type of card
        cardrequest = CardRequest( timeout=1, cardType=cardtype )

        print("Waiting for card")
        cardservice = cardrequest.waitforcard()
        print("Card connected")

        # connecting to card
        cardservice.connection.connect()
        # cardservice.connection.connect( CardConnection.T1_protocol) # Connecting with a specific T1 or T2 protocol

        print("connected to reader: " + str(cardservice.connection.getReader()))
        print("connected to card (in bytes): " + str(cardservice.connection.getATR()))
        print("connected to card (in hex): " + str(toHexString(cardservice.connection.getATR())))
        print("this is my card") if cardservice.connection.getATR() == mycardbytes else print("this is not my card")

        return NFCconnection(
            cardservice = cardservice,
        )

    def get_handshake(self):
        #ACS ACR122U NFC Reader
        #Suprisingly, to get data from the tag, it is a handshake protocol
        #You send it a command to get data back
        #This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
        
        # it basically returns the UID of the card
        handshake = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer

        response, sw1, sw2 = self.cardservice.connection.transmit(handshake)
        if sw1 == 144:
            print(f"Handshake with card succesfull!")
        else:
            print(f"Handshake failed!")

        return response

    def read_card(self):
        
        # get handshake first
        response = self.get_handshake()
        responsehex = toHexString(response)
        print(f"UID of card is: {response}")

        data = ""
        page = 1
        while page > 0 and page < 10:
            try:
                readdata = self.read_page(page)
                print(f"retrieving page {page} resulted in {readdata}")
                data += readdata
                page += 1
            except:
                page = 0

        print(f"data of whole card is: {data}")
        return data

    def read_page(self, page):

        #Read command [FF, B0, 00, page, #bytes]
        print(f"trying to retrieve page {page}")
        response, sw1, sw2 = self.cardservice.connection.transmit([0xFF, 0xB0, 0x00, page, 0x04])
        print(f"response: {response} status words: {sw1} {sw2}")

        return response

    def read_card_depreciated(self, op_type):
    
        ISOAPDU=  {
            'ERASE BINARY':'0E',
            'VERIFY':'20',
            # Global Platform
            'INITIALIZE_UPDATE':'50',
            # GP end
                    'MANAGE_CHANNEL':'70',
                    'EXTERNAL_AUTHENTICATE':'82',
                    'GET_CHALLENGE':'84',
                    'INTERNAL_AUTHENTICATE':'88',
                    'SELECT_FILE':'A4',
                    #vonjeek start
                    'VONJEEK_SELECT_FILE':'A5',
                    'VONJEEK_UPDATE_BINARY':'A6',
                    'VONJEEK_SET_MRZ':'A7',
            'VONJEEK_SET_BAC':'A8',
            'VONJEEK_SET_DATASET':'AA',
                    #vonjeek end
            # special for JCOP
            'MIFARE_ACCESS':'AA',
            'ATR_HIST':'AB',
            'SET_RANDOM_UID':'AC',
            # JCOP end
                    'READ_BINARY':'B0',
                    'READ_RECORD(S)':'B2',
                    'GET_RESPONSE':'C0',
                    'ENVELOPE':'C2',
                    'GET_DATA':'CA',
                    'WRITE_BINARY':'D0',
                    'WRITE_RECORD':'D2',
                    'UPDATE_BINARY':'D6',
                    'PUT_DATA':'DA',
                    'UPDATE_DATA':'DC',
            'CREATE_FILE':'E0',
                    'APPEND_RECORD':'E2',
            # Global Platform
            'GET_STATUS':'F2',
            # GP end
            'READ_BALANCE':'4C',
            'INIT_LOAD': '40',
            'LOAD_CMD':'42',
            'WRITE_MEMORY':'7A',
            'READ_MEMORY':'78',
            }

        # COMMAND : [Class, Ins, P1, P2, DATA, LEN]
        PCSC_APDU= {
            'ACS_14443_A' : ['d4','40','01'],
            'ACS_14443_B' : ['d4','42','02'],
            'ACS_14443_0' : ['d5','86','80', '05'],
            'ACS_DISABLE_AUTO_POLL' : ['ff','00','51','3f','00'],
            'ACS_DIRECT_TRANSMIT' : ['ff','00','00','00'],
            'ACS_GET_SAM_SERIAL' : ['80','14','00','00','08'],
            'ACS_GET_SAM_ID' : ['80','14','04','00','06'],
            'ACS_GET_READER_FIRMWARE' : ['ff','00','48','00','00'],
            'ACS_GET_RESPONSE' : ['ff','c0','00','00'],
            'ACS_GET_STATUS' : ['d4','04'],
            'ACS_IN_LIST_PASSIVE_TARGET' : ['d4','4a'],
            'ACS_LED_GREEN' : ['ff','00','40','0e','04','00','00','00','00'],
            'ACS_LED_ORANGE' : ['ff','00','40','0f','04','00','00','00','00'],
            'ACS_LED_RED' : ['ff','00','40','0d','04','00','00','00','00'],
            'ACS_MIFARE_LOGIN' : ['d4','40','01'],
            'ACS_READ_MIFARE' : ['d4','40','01','30'],
            'ACS_POLL_MIFARE' : ['d4','4a','01','00'],
            'ACS_POWER_OFF' : ['d4','32','01','00'],
            'ACS_POWER_ON' : ['d4','32','01','01'],
            'ACS_RATS_14443_4_OFF' : ['d4','12','24'],
            'ACS_RATS_14443_4_ON' : ['d4','12','34'],
            'ACS_SET_PARAMETERS' : ['d4','12'],
            'ACS_SET_RETRY' : ['d4','32','05','00','00','00'],
            'AUTHENTICATE' : ['ff', ISOAPDU['INTERNAL_AUTHENTICATE']],
            'GUID' : ['ff', ISOAPDU['GET_DATA'], '00', '00', '00'],
            'ACS_GET_ATS' : ['ff', ISOAPDU['GET_DATA'], '01', '00', '00'],
            'LOAD_KEY' : ['ff',  ISOAPDU['EXTERNAL_AUTHENTICATE']],
            'READ_BLOCK' : ['ff', ISOAPDU['READ_BINARY']],
            'UPDATE_BLOCK' : ['ff', ISOAPDU['UPDATE_BINARY']],
            'VERIFY' : ['ff', ISOAPDU['VERIFY']],
            'WRITE_BLOCK' : ['ff', ISOAPDU['WRITE_BINARY']],
            }

        # in order to log the details of the op_type variable we translate the bytes to hex so they become human readable
        op_typehex = []
        for i in op_type:
            hexstring = hex(i)
            hexstring12 = hexstring[0] + hexstring[1]
            if len(hexstring) == 3:
                hexstring34 = hexstring[2].upper() + "0"
            else:
                hexstring34 = hexstring[2].upper() + hexstring[3].upper()
            hexstring = hexstring12 + hexstring34
            op_typehex += [hexstring]

        print(f"op_type hex: {op_typehex}")
        print(f"op_type: {op_type}")

        # use the following details (in tutorial DF_TELECOM)
        # op_details = [0x05, 0x00, 0x00, 0x00, 0x00, 0x00]

        # in order to log the details of the op_details variable we translate the bytes to hex so they become human readable
        # op_detailshex = []
        # for i in op_details:
        #     hexstring = hex(i)
        #     hexstring12 = hexstring[0] + hexstring[1]
        #     if len(hexstring) == 3:
        #         hexstring34 = hexstring[2].upper() + "0"
        #     else:
        #         hexstring34 = hexstring[2].upper() + hexstring[3].upper()
        #     hexstring = hexstring12 + hexstring34
        #     op_detailshex += [hexstring]

        # print(f"op_details hex: {op_detailshex}")
        # print(f"op_details: {op_details}")

        apdu = op_type # + op_details
        print(f"sending {toHexString(apdu)}")

        # response, sw1, sw2 = cardservice.connection.transmit( apdu, CardConnection.T1_protocol )
        response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
        print(f"response: {response} status words: {sw1} {sw2}")

        return response