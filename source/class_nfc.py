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

import ndef
# from ndef.message import message_decoder, message_encoder
# from ndef.record import Record

from .class_conversions import (
    ConvertingArrays,
    ConvertingNumbers,
    EncodingCharacter,
    DecodingCharacter,
)

class NDEFcoding(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def decode_message(response):
        """creates a list of records that is found on the card, expects a response in the form of a byte array that can be interpreted as ndef format"""

        # print(f"input response = {response}")
        
        octets = response
        # print(f"octets = {octets}")

        decoder = ndef.message_decoder(octets)
        # print(f"decoder = {decoder}")
        
        message = list(decoder)
        # print(f"message = {message}")

        for _ in decoder:
            next(decoder)

        return message

    @staticmethod
    def encode_message(data):
        """creates an ndef encoding to write to the card, needs a data of a certain type to encode it to ndef format"""

        # ndeflib example
        print(data)
        databin= data.encode('utf-8')
        print(databin)
        record = ndef.Record('urn:nfc:wkt:T', '1', databin)
        payload = ndef.message_encoder(record)
        print(f"encoded payload = {payload}")

        return payload

class NFCreference(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_reference_material():

        # set the paths to the apdu reference file
        path = os.path.join(os.path.dirname(__file__), "..", "references") # the same folder as caller
        filename = "nfc_communication"
        complete_path = os.path.join(path, filename + ".json")

        # open file and return the dictionary
        with open(complete_path, 'r') as infile:
            datadict = json.load(infile)
        
        return datadict

class NFCconnection(object):
    def __init__(self, cardservice):
        super().__init__()
        self.cardservice = cardservice

    @staticmethod
    def initialize(card_type = ""):

        if card_type == "":
            cardtype = AnyCardType() # for accepting any type of card
        else:
            cardtype = ATRCardType(card_type)
        
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

        nfc_connection = NFCconnection(cardservice = cardservice)

        # get some info out of ATR:
        atr_info = nfc_connection.get_atr_info()
        print(f"ATR information is: {atr_info}")
        print("")

        response, responsehex = nfc_connection.identify_card()
        print(f"UID of card is: {response} with hex: {responsehex}")
        print("")

        return nfc_connection

    @staticmethod
    def initialize_any():

        nfc_connection = NFCconnection.initialize()

        return nfc_connection

    @staticmethod
    def initialize_specific(exp_atr):

        nfc_connection = NFCconnection.initialize(exp_atr)

        return nfc_connection

    def get_atr_info(self):

        atr = self.cardservice.connection.getATR()
        
        datadict = NFCreference.get_reference_material()
        atrdict = datadict["ATR (Anwser To Reset)"]

        # the block length
        length = 0
        info = "length"
        length_value = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        # "OC" apparantly means 12 bytes of config data as C is the 12th letter in the hexadecimal numbering
        # print(f"length_string: {length_string}")
        length = f"{length_value}"


        # RID or Registered App Provider Identifier
        rid = "Unknown"
        info = "Registered App Provider Identifiers (RIDs)"
        atrsplit = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        rid_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        known_values = atrdict[info]["Known values"]
        for key in known_values:
            if known_values[key] == rid_string:
                rid = f"{key}"
                break

        if rid == "Unknown":
            rid += f" - RID code: -{rid_string}-"


        # Standard
        standard = "Unknown"
        info = "Standards"
        atrsplit = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        standard_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        known_values = atrdict[info]["Known values"]
        for key in known_values:
            if known_values[key] == standard_string:
                standard = f"{key}"
                break
        
        if standard == "Unknown":
            standard += f" - standard code: -{standard_string}-"


        # card ty0pes
        card_type = "Unknown"
        info = "Card Types"
        atrsplit = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        card_type_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        known_values = atrdict[info]["Known values"]
        for key in known_values:
            if known_values[key] == card_type_string:
                card_type = f"{key}"
                break
        
        if card_type == "Unknown":
            card_type += f" - card name code: -{card_type_string}-"



        # something to do with clock frequencies, are often left at 0 to set default setting.
        rfu = "Unknown"
        info = "Radio Frequency Units (RFUs)"
        atrsplit = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        rfu_string = ConvertingArrays.array_conversion(atrsplit, "int_to_hex")

        known_values = atrdict[info]["Known values"]
        for key in known_values:
            if known_values[key] == rfu_string:
                rfu = f"{key}"
                break
        
        if rfu == "Unknown":
            rfu += f" - card name code: -{rfu_string}-"

        return {"length": length, "rid": rid, "standard": standard, "card_type": card_type, "rfu": rfu}

    def get_apdu_command(self, function):
    
        datadict = NFCreference.get_reference_material()

        atr_info = self.get_atr_info()
        card_type = atr_info["card_type"]

        apdu_command = "Card not recognized!"
        for key in datadict:
            if key == card_type:
                for key2 in datadict[key]:
                    if key2 == function:
                        apdu_command = datadict[key][key2]["APDU_int"]
                
        return apdu_command

    def identify_card(self):
        #ACS ACR122U NFC Reader
        #This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
        
        # it basically returns the UID of the card, for some cards this is necassary to open for communication (aka handshake)
        apdu_command = self.get_apdu_command("Identify")

        response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
        if sw1 == 144 and sw2 == 0:
            print(f"Handshake with card succesfull!")
        else:
            print(f"Handshake failed!")

        responsehex = ConvertingArrays.array_conversion(response, "int_to_hex")

        return response, responsehex

    def read_card(self):
        
        # retrieving raw data (integer array) from card
        data = []
        page = 1
        while page > 0 and page < 45:
            apdu_command = self.get_apdu_command("Read")
            apdu_command[3] = page
            # print(f"sending read command: {apdu_command}")
            # print(f"trying to retrieve page {page}")
            response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
            # print(f"response: {response} status words: {sw1} {sw2}")
            data += response
            page += 1
        # print(f"Raw data of card is: {data}")
        # print("")

        # converting the raw data to hex string
        datahexarray = ConvertingArrays.array_conversion(data, "int_to_hex")
        datahex = ""
        for i in datahexarray:
            datahex += ConvertingNumbers.hex_to_hexstr(i)
        # print(f"hex data is: {datahex}")
        # print("")

        # find payload part
        index_start = datahex.find("5402656e") - 6
        index_end = datahex.find("fe")
        payload = datahex[index_start:index_end]
        # print(f"ndef data is: {payload}")
        # print("")
        
        # decode payload
        databytearray = bytearray.fromhex(payload)
        payloadobject = NDEFcoding.decode_message(databytearray)
        # print(f"returned payloadobject: {payloadobject}")
        # print("")

        payload = {}
        i = 0
        for dataobject in payloadobject:
            i += 1
            if dataobject.type == "urn:nfc:wkt:T":
                stripped = dataobject.data[3:]
                decoded = stripped.decode('UTF-8')
                payload.update({i: decoded})
        print(f"payload with {i} records: {payload}")
        print("")

        return payload

    def write_card(self, data):

        # prepare data
        NDEFcoding.encode_message(data)


        # prepare data command
        apdu_command = self.get_apdu_command("Write")


        WRITE_COMMAND = [apdu_command, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
        # # Let's write a page Page 9 is usually 00000000
        # response, sw1, sw2 = connection.transmit(WRITE_COMMAND)
    



# class NFCdecoder(object):
#     """depreciated"""
#     def __init__(self):
#         super().__init__()

#     @staticmethod
#     def decode_message(response):

#         print(f"trying to decode {response}")
#         response_hex = []
#         message = ""
#         for page in response:
#             pagehex = []
#             pagestring = ""
#             for i in page:
#                 hexa = ConvertingNumbers.int_to_hex(i)
#                 pagehex += [hexa]
#                 character = DecodingCharacter.integer_to_character(i)
#                 pagestring += character
#             # print(f"Page {page} decoded to {pagestring}")
#             response_hex += [pagehex]
#             message += pagestring
#         print(f"response in hex: {response_hex}")
#         print(f"Decoded message: {message}")

#         return response_hex, message
