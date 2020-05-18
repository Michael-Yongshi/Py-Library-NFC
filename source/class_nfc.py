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

        print(f"trying to encode {data}")
        # encode characters to bytes
        databin= data.encode('utf-8')
        # print(databin)
        # ndeflib example
        record = ndef.Record('urn:nfc:wkt:T', '1', databin)
        # no clue yet why below works as it does. the last line actually returns / yields the record from the previous line
        encoder = ndef.message_encoder()
        encoder.send(None)
        encoder.send(record)
        payload = encoder.send(None)
        # payload = ndef.message_encoder(record)
        # print(f"encoded payload = {payload}")

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

        # print("Waiting for card")
        cardservice = cardrequest.waitforcard()
        # print("Card found")

        # connecting to card
        cardservice.connection.connect()
        print("Success: NFC Connection established")


        reader = cardservice.connection.getReader()
        # print(f"connected to reader: {reader}")
        atr = cardservice.connection.getATR()
        # print(f"connected to card (in bytes): {str(atr)}")
        atrhex = ConvertingArrays.array_conversion(atr, "int_to_hex")
        # print(f"connected to card (in hex): {str(atrhex)}")

        nfc_connection = NFCconnection(cardservice = cardservice)

        # set ATR information to variable:
        nfc_connection.get_atr_info()
        # print(f"ATR information is: {self.atr_info}")

        response, responsehex = nfc_connection.identify_card()
        # print(f"UID of card is: {response} with hex: {responsehex}")

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

        self.atr_info = {"length": length, "rid": rid, "standard": standard, "card_type": card_type, "rfu": rfu}

        return self.atr_info

    def get_apdu_command(self, function):
    
        datadict = NFCreference.get_reference_material()

        card_type = self.atr_info["card_type"]

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

        # converting the raw data to hex string
        # datahexarray = ConvertingArrays.array_conversion(data, "int_to_hex")
        # datahex = ""
        # for i in datahexarray:
        #     datahex += ConvertingNumbers.hex_to_hexstr(i)
        # print(f"hex data is: {datahex}")

        # find payload part
        for idx, val in enumerate(data):
            # print(idx, val)
            if val == 254:
                index_end = idx
                # print(index_end)
                break
            elif idx > len(data) -4:
                pass
            elif [val, data[idx+1], data[idx+2], data[idx+3]] == [84, 2, 101, 110]:
                index_start = idx+4
                # print(index_start)
            else:
                pass

        payload = data[index_start:index_end]
        # print(f"payload is: {payload}")

        # decode payload
        encrypted_key = bytes(payload)

        print(f"Success: NFC payload: {encrypted_key}")

        return encrypted_key

    def write_card(self, data, encode=True):

        # print(f"data to be written = {data}")

        # prepare data
        recordlength = len(data) + 7
        datalength = len(data) + 3
        datalist = list(data)
        # print(f"data in list form = {datalist}")
        databytes = bytes(data)
        # print(f"data in bytes form = {databytes}")
        payload = [3, recordlength, 209, 1, datalength, 84, 2, 101, 110] + list(data) + [254]
        # print(f"payload data = {payload}")

        payloadlength = len(payload)
        page = 4
        try:
            for i in range(0, payloadlength - 1, 4):
                # prepare data command
                write_command = self.get_apdu_command("Write")
                write_command[3] = page
                apdu = write_command + payload[i:i+4]
                # print(f"apdu = {apdu}")
                # apdu_hex = ConvertingArrays.array_conversion(apdu, "int_to_hex")
                # print(f"apdu in hex = {apdu_hex}")

                response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
                # print(f"response: {response}, sw1 = {sw1}, sw2 = {sw2}")

                page += 1

            print(f"Success: NFC written to card: {payload}")
        except:
            print(f"Failed: NFC is not written correctly")
