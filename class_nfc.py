# https://pyscard.sourceforge.io/user-guide.html
# Sample script for the card centric approach

import os
import json
import codecs

from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.System import readers

from .class_conversions import (
    ConvertingArrays,
    ConvertingNumbers,
    EncodingCharacter,
    DecodingCharacter,
)

class NFCreference(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_apdu_command(function):
    
        # set the paths to the apdu reference file
        path = os.path.join(os.path.dirname(__file__), "references") # the same folder as caller
        filename = "nfc_communication"
        complete_path = os.path.join(path, filename + ".json")

        # open file and return the dictionary
        with open(complete_path, 'r') as infile:
            datadict = json.load(infile)

        for key in datadict:
            if key == "Mifare Ultralight":
                for key2 in datadict[key]:
                    if key2 == function:
                        apdu_command = datadict[key][key2]["APDU_int"]
                
        return apdu_command

    @staticmethod
    def get_card_block_length(atr):
        # the block length
        length = "Unknown"
 
        length_value = atr[6]
        # "OC" apparantly means 12 bytes of config data as C is the 12th letter in the hexadecimal numbering
        # print(f"length_string: {length_string}")
     
        length = f" - length code: {length_value}"

        return length

    @staticmethod
    def get_card_rid(atr):
        # also known as RID or Registered App Provider Identifier
        rid = "Unknown"

        rids = {
            "0XA0 0X0 0X0 0X3 0X6": "PC/SC Workgroup",
        }

        # 9th position, pythons first position is 0, so 9-1=8
        atrsplit = atr[7:12]
        rid_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        # print(f"rid_string: {rid_string}")

        for key in rids:
            if key == rid_string:
                rid = f"{rids[key]} (code: {key})"
                break
    
        if rid == "Unknown":
            rid += f" - RID code: -{rid_string}-"

        return rid

    @staticmethod
    def get_card_standard(atr):
        # the iso standard that is followed
        standard = "Unknown"

        standards = {
            "0X3": "ISO14443A, Part3", # standard format
        }

        # 
        # 9th position, pythons first position is 0, so 9-1=8
        atrsplit = atr[12:13]
        standard_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        # print(f"standard_string: {standard_string}")

        for key in standards:
            if key == standard_string:
                standard = f"{standards[key]} (code: {key})"
                break
        
        if standard == "Unknown":
            standard += f" - standard code: -{standard_string}-"

        return standard

    @staticmethod
    def get_card_type(atr):

        card_type = "Unknown"

        card_types = {
            "0X0 0X1": "Mifare 1K",
            "0X0 0X2": "Mifare 4k",
            "0X0 0X3": "Mifare Ultralight",
            "0X0 0X26": "Mifare Mini",
            "0XF0 0X4": "Topaz and Jewel",
            "0XF0 0X11": "Felica 212k",
            "0XF0 0X12": "Felica 424k",
        }

        atrsplit = atr[13:15]
        card_type_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        for key in card_types:
            if key == card_type_string:
                card_type = f"{card_types[key]} (code: {key})"
                break
        
        if card_type == "Unknown":
            card_type += f" - card name code: -{card_type_string}-"

        return card_type

    @staticmethod
    def get_card_rfu(atr):
        # something to do with clock frequencies, are often left at 0 to set default setting.
        rfu = "Unknown"

        rfus = {
            "0X0 0X0 0X0 0X0": "Default setting",
        }

        atrsplit = atr[15:19]
        rfu_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        for key in rfus:
            if key == rfu_string:
                rfu = f"{rfus[key]} (code: {key})"
                break
        
        if rfu == "Unknown":
            rfu += f" - card name code: -{rfu_string}-"

        return rfu

class NDEFinterpreter(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def decode_message(response):

        print(f"trying to decode {response}")
        response_hex = []
        message = ""
        for page in response:
            pagehex = []
            pagestring = ""
            for i in page:
                hexa = ConvertingNumbers.int_to_hex(i)
                pagehex += [hexa]
                character = DecodingCharacter.integer_to_character(i)
                pagestring += character
            # print(f"Page {page} decoded to {pagestring}")
            response_hex += [pagehex]
            message += pagestring
        print(f"response in hex: {response_hex}")
        print(f"Decoded message: {message}")

        return response_hex, message

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
        atrhex = ConvertingArrays.array_conversion(atr, "int_to_hex")
        print(f"connected to card (in hex): {str(atrhex)}")
        print("")

        # get some info out of ATR:
        length = NFCreference.get_card_block_length(atr)
        print(f"byte 7 // config data length: {length}")
        rid = NFCreference.get_card_rid(atr)
        print(f"bytes 8 - 12 // rid: {rid}")
        standard = NFCreference.get_card_standard(atr)
        print(f"byte 13 // standard: {standard}")
        card_type = NFCreference.get_card_type(atr)
        print(f"bytes 14 - 15 // cardtype: {card_type}")
        rfu = NFCreference.get_card_rfu(atr)
        print(f"bytes 16 - 19 // rfu: {rfu}")

        return NFCconnection(
            cardservice = cardservice,
        )

    @staticmethod
    def initialize_specific(atr, atrhex):

        # Sample script for the smartcard.ATR utility class.
        mycardbytes = NFCmethods.hexstring_to_bytes(atr)
        cardtype = ATRCardType(mycardbytes) # for accepting a specific type of card
        cardrequest = CardRequest( timeout=1, cardType=cardtype )

        print("Waiting for card")
        cardservice = cardrequest.waitforcard()
        print("Card connected")

        # connecting to card
        cardservice.connection.connect()

        print("this is my card") if cardservice.connection.getATR() == mycardbytes else print("this is not my card")

        return NFCconnection(
            cardservice = cardservice,
        )

    def get_card_uid(self):
        #ACS ACR122U NFC Reader
        #This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
        
        # it basically returns the UID of the card
        # apdu_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        apdu_command = NFCreference.get_apdu_command("Identify")

        response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
        if sw1 == 144 and sw2 == 0:
            print(f"Handshake with card succesfull!")
        else:
            print(f"Handshake failed!")

        responsehex = ConvertingArrays.array_conversion(response, "int_to_hex")

        print(f"UID of card is: {response} with hex: {responsehex}")

        return response, responsehex

    def get_card_data(self):
        
        data = []
        page = 1
        while page > 0 and page < 45:
            try:
                readdata = self.get_card_page(page)
                data += [readdata]
                page += 1
            except:
                page = 0

        print(f"data of whole card is: {data}")
        return data

    def get_card_page(self, page):

        apdu_command = NFCreference.get_apdu_command("Read")
        apdu_command[3] = page

        print(f"sending read command: {apdu_command}")
        # apdu_command = [0xFF, 0xB0, 0x00, int(page), 0x04]

        # print(f"trying to retrieve page {page}")
        response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
        # print(f"response: {response} status words: {sw1} {sw2}")

        return response

    def set_card_data(self):
        
        page = 1
        while page > 0 and page < 2:
            self.set_card_page(page)
        
    def set_card_page(self, page):

        apdu_command = NFCreference.get_apdu_command("set_card_page")
        apdu_command.append(page)
        apdu_command.append(0x04)
        apdu_command_static = [0xFF, 0xD6, 0x00, int(page), 0x04]
        print(f"apdu dynamic = {apdu_command}, while apdu static = {apdu_command_static}")

        # WRITE_COMMAND = [apdu_command, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
        # # Let's write a page Page 9 is usually 00000000
        # response, sw1, sw2 = connection.transmit(WRITE_COMMAND)

    # def read_card_depreciated(self, op_type):
    # 


    #     # in order to log the details of the op_type variable we translate the bytes to hex so they become human readable
    #     op_typehex = []
    #     for i in op_type:
    #         hexstring = hex(i)
    #         hexstring12 = hexstring[0] + hexstring[1]
    #         if len(hexstring) == 3:
    #             hexstring34 = hexstring[2].upper() + "0"
    #         else:
    #             hexstring34 = hexstring[2].upper() + hexstring[3].upper()
    #         hexstring = hexstring12 + hexstring34
    #         op_typehex += [hexstring]

    #     print(f"op_type hex: {op_typehex}")
    #     print(f"op_type: {op_type}")

    #     # use the following details (in tutorial DF_TELECOM)
    #     # op_details = [0x05, 0x00, 0x00, 0x00, 0x00, 0x00]

    #     # in order to log the details of the op_details variable we translate the bytes to hex so they become human readable
    #     # op_detailshex = []
    #     # for i in op_details:
    #     #     hexstring = hex(i)
    #     #     hexstring12 = hexstring[0] + hexstring[1]
    #     #     if len(hexstring) == 3:
    #     #         hexstring34 = hexstring[2].upper() + "0"
    #     #     else:
    #     #         hexstring34 = hexstring[2].upper() + hexstring[3].upper()
    #     #     hexstring = hexstring12 + hexstring34
    #     #     op_detailshex += [hexstring]

    #     # print(f"op_details hex: {op_detailshex}")
    #     # print(f"op_details: {op_details}")

    #     apdu = op_type # + op_details
    #     print(f"sending {NFCmethods.bytes_to_hex(apdu)}")

    #     # response, sw1, sw2 = cardservice.connection.transmit( apdu, CardConnection.T1_protocol )
    #     response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
    #     print(f"response: {response} status words: {sw1} {sw2}")

    #     return response