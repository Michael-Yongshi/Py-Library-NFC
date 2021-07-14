# https://pyscard.sourceforge.io/user-guide.html
# Sample script for the card centric approach

import os
import codecs

import ndef
import json
from time import sleep

from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.System import readers
from smartcard.util import toBytes

from .class_conversions import (
    ConvertingArrays,
    ConvertingNumbers,
    EncodingCharacter,
    DecodingCharacter,
)

class NFCconnection(object):
    def __init__(self, cardservice, metadata):
        super().__init__()
        self.cardservice = cardservice
        self.metadata = metadata

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
        reader = cardservice.connection.getReader()
        print(f"Success: NFC Connection established on reader {reader}")

        # set up object
        nfc_connection = NFCconnection(
            cardservice = cardservice,
            metadata = {},
        )

        # add reader info to object
        nfc_connection.metadata['reader'] = reader

        # to make next command more robust
        sleep(0.1)

        # get metadata
        nfc_connection.get_card_atr_info()
        nfc_connection.get_card_uid()
        nfc_connection.get_card_size()

        uid = nfc_connection.metadata["UID"]
        size = nfc_connection.metadata["Size"]
        card_type = nfc_connection.metadata['ATR']['card_type']
        card_subtype = nfc_connection.metadata['ATR']['card_subtype']
        print(f"Success: NFC Connection identified as {uid} with size {size},card:{card_type}/{card_subtype}")

        return nfc_connection

    def get_reference_material(self):

        # # set the paths to the apdu reference file
        path = os.path.join(os.path.dirname(__file__)) # the same folder as caller
        filename = "nfc_communication"
        complete_path = os.path.join(path, filename + ".json")

        # open file and return the dictionary
        with open(complete_path, 'r') as infile:
            datadict = json.load(infile)

        # print(datadict)
        # return datadict

        # datadict = {'ATR (Anwser To Reset)': {'start byte': {'start': 0, 'end': 1}, 'historical byte count': {'start': 1, 'end': 2}, 'length': {'start': 6, 'end': 7}, 'Registered App Provider Identifiers (RIDs)': {'start': 7, 'end': 12, 'Known values': {'PC/SC Workgroup': ['0xa0', '0x0', '0x0', '0x3', '0x6'], '': ''}}, 'Standards': {'start': 12, 'end': 13, 'Known values': {'ISO14443A, Part3': ['0x3'], '': ''}}, 'Card Types': {'start': 13, 'end': 15, 'Known values': {'Mifare 1K': ['0x0', '0x1'], 'Mifare 4k': ['0x0', '0x2'], 'Mifare Ultralight': ['0x0', '0x3'], 'Mifare Mini': ['0x0', '0x26'], 'Topaz and Jewel': ['0xF0', '0x4'], 'Felica 212k': ['0xF0', '0x11'], 'Felica 424k': ['0xF0', '0x12']}}, 'Radio Frequency Units (RFUs)': {'start': 15, 'end': 19, 'Known values': {'Default setting': ['0x0', '0x0', '0x0', '0x0'], '': ''}}}, 'Mifare Ultralight': {'Identify': {'APDU_int': [255, 202, 0, 0, 0], 'APDU_hex': ['0xFF', '0xCA', '0x0', '0x0', '0x0'], 'Response': {}}, 'Read': {'APDU_int': [255, 176, 0, 'block', 4], 'APDU_hex': ['0xFF', '0xB0', '0x0', 'block', '0x4'], 'Response': {'text': {'start': {'block': 6, 'byte': 3}, 'end': {'type': 'encounter', 'at': 254}}}}, 'Write': {'APDU_int': [255, 214, 0, 'block', 4], 'APDU_hex': ['0xFF', '0xD6', '0x0', 'block', '0x4'], 'Response': {'text': {'start': {'block': 6, 'byte': 3}, 'end': {'type': 'encounter', 'at': 254}}}}}}

        # print(datadict)
        return datadict

    def get_card_atr_info(self):

        datadict = self.get_reference_material()
        atrdict = datadict["ATR (Anwser To Reset)"]

        atr = self.cardservice.connection.getATR()

        # 1 point: Start byte
        info = "start byte"
        atr_split = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        atr_point = atr_split[0]

        # 2 point: Historical byte count
        #second character, first digit (in 8f, the f)
        info = "historical byte count"
        atr_split = atr[atrdict[info]["start"]:atrdict[info]["end"]]
        atr_point = atr_split[0]
        atr_point_hex = ConvertingNumbers.int_to_hex(atr_point)
        hist_byte_count_hex = atr_point_hex[-1:]
        hist_byte_count = ConvertingNumbers.hex_to_int(hist_byte_count_hex)

        atr_point_bit = ConvertingNumbers.int_to_bit(atr_point)
        # print(atr_point_bit)

        # 3 point: 
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


        # card types
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

        subtype = "Unknown"
        size = None
        if card_type in ["Mifare Ultralight EV1","Mifare Ultralight"]: # only tested on omnikey 5022CL and ACR122U
            offset = 2
            data_hex = "FF"
            if "OMNIKEY 5022" in self.metadata["reader"]: 
                data_hex = "FF680E030B1F08000000000000000060"
            elif "ACR122" in self.metadata["reader"]:
                offset = 3
                data_hex = "FF00000003D44260"

            data = toBytes(data_hex)
            apdu_command = data
            response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
            if sw1 == 144:
                (vender_id, product_type,product_subtype, major_version, storage_code) = (response[offset + 1],
                    response[offset + 2 ],response[offset+3],response[offset+4],response[offset+6])
                if vender_id == 4:
                    vender = "NXP" 
                if product_type == 4: # General NTAG
                    subtype = "NTAG"
                    if major_version == 1: # NTAG210, 212,213,215,216
                        if product_subtype == 0x01: # 17pF ,NTAG210,212
                            if storage_code == 0x0B:
                                subtype = "NTAG210"
                                size = 48
                            if storage_code == 0x0E:
                                subtype = "NTAG212"
                                size = 128
                        if product_subtype == 0x02: # 50pF, NTAG213,215,216
                            if storage_code == 0x0F:
                                subtype = "NTAG213"
                                size = 144 
                            if storage_code == 0x11:
                                subtype = "NTAG215"
                                size = 504
                            if storage_code == 0x13:
                                subtype = "NTAG216"
                                size = 888
                    if major_version == 3: #NTAG213TT
                        if storage_code == 0x0F:
                            subtype = "NTAG213TT"
                            size =  144

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

        atr_info = {"ATRraw": atr, "hist byte count": hist_byte_count, "length": length, "rid": rid, "standard": standard, 
        "card_type": card_type, "rfu": rfu, "card_subtype": subtype}

        self.metadata = {"ATR": atr_info}

        if size != None:
            self.metadata.update({"Size": size})

    def get_card_uid(self):

        #ACS ACR122U NFC Reader
        #This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
        # it basically returns the UID of the card, for some cards this is necassary to open for communication (aka handshake)

        # retrieve UID of card
        apdu_command = self.get_apdu_command("Identify")
        response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
        responsehex = ConvertingArrays.array_conversion(response, "int_to_hex")

        self.metadata.update({"UID": response})

    def get_card_size(self):

        card_type = self.metadata["ATR"]["card_type"]
        subtype = self.metadata["ATR"]["card_subtype"]

        # retrieving length of card
        page = 1
        sw1 = 144
        while sw1 == 144:
            apdu_command = self.get_apdu_command("Read")
            apdu_command[3] = page
            response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
            page += 1
        pages = page - 10
        print(f"size in pages = {pages}")

        size = pages * 4
        print(f"size in bytes = {size}")

        if card_type in ["Mifare Ultralight EV1","Mifare Ultralight"] and "NTAG" in subtype:
            return
        else:
            self.metadata.update({"Size": size})

    def get_apdu_command(self, function):

        datadict = self.get_reference_material()

        card_type = self.metadata["ATR"]["card_type"]

        apdu_command = "Card not recognized!"
        for key in datadict:
            if key == card_type:
                for key2 in datadict[key]:
                    if key2 == function:
                        apdu_command = datadict[key][key2]["APDU_int"]

        return apdu_command

    def read_card(self):
        """
        Read the whole payload of the card
        """

        # get size of card
        size = self.metadata["Size"]
        pages = size / 4
        # print(size)

        # Handshake with card 
        self.get_card_uid()

        # retrieving raw data (integer array) from card
        data = []
        page = 4
        while page <= pages: # read only the relative to the size of the card (leave the last 5 pages alone, they are not data fields, but are writable)
            
            data += self.read_card_raw(page=page)
            page += 1

        # print(f"{page - 1} pages read")

        index_start = 0
        index_end = len(data) - 1

        # if successfull find payload part
        for idx, val in enumerate(data):
            # print(idx, val)
            if val == 254:
                index_end = idx
                # print(index_end)
                break
            elif idx > len(data) -4:
                pass
            # elif [val, data[idx+1], data[idx+2], data[idx+3]] == [84, 2, 101, 110]:
            #     index_start = idx+4
                # print(index_start)
            else:
                pass

        print(f"Read payload in bytes: {data}")
        payload = data[2:index_end]
        # print(f"payload is: {payload}")

        # decode payload
        data = bytes(payload)

        print(f"Success: NFC payload read from card")

        return data

    def read_card_raw(self, page=4):
        '''
        Read raw data from the card
        If page is not given will get the first block of data (which is page 4)
        '''

        apdu_command = self.get_apdu_command("Read")
        apdu_command[3] = page
        response, sw1, sw2 = self.cardservice.connection.transmit(apdu_command)
        # print(f"page: {page}, response: {response}, status words: {sw1} : {sw2}")
        if sw1 == 99:
            print(f"Failed reading card at page {page}, response {response}, sw1 {sw1}, sw2 {sw2}")
            return
        print(f"read data:{response}")
        data = bytes(response)

        return data

    def wipe_card(self):

        # get size of card
        size = self.metadata["Size"]
        # print(size)

        # Handshake with card 
        self.get_card_uid()

        page = 4
        while page <= size: # wipe only the relative to the size of the card (leave the last 5 pages alone, they are not data fields, but are writable)
            # prepare data command
            write_command = self.get_apdu_command("Write")
            write_command[3] = page
            apdu = write_command + [0, 0, 0, 0]
            # print(f"apdu = {apdu}")
            # apdu_hex = ConvertingArrays.array_conversion(apdu, "int_to_hex")
            # print(f"apdu in hex = {apdu_hex}")

            response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
            # print(f"response: {response}, sw1 = {sw1}, sw2 = {sw2}")

            if sw1 == 99:
                print(f"Failed: NFC wipe at page {page} failed, response {response}, sw1 {sw1}, sw2 {sw2}")
                return "Failed"
            page += 1

        print(f"Success: NFC card is wiped")
        return "Success"

    def write_card(self, data):
        """
        checks payload and card before writing raw data to card for a default writing action
        """

        # get size of card
        size = self.metadata["Size"]
        # print(size)

        # Convert to bytes if necessary
        databytes = convert_data_to_bytes(data)

        # metadata of payload
        recordlength = len(databytes)

        if recordlength > size:
            print("Failed: card size is too small for payload")

        result = self.write_card_raw(databytes=databytes)

        if result == "Success":
            print(f"Success: data written to card: {data}")
            return "Success"
        else:
            print(f"Failed")
            return "Failed"

    def write_card_raw(self, databytes, pagestart = 4):
        '''
        Write raw data onto the card
        Expects a bytes object that is directly writable.
        Optional note the starting block of the nfc with an integer in 'pagestart', by default starts at data blocks (page 4)

        To write a string or integer variable first use the method 'convert_data_to_bytes' to convert a string or integer to a bytes object
        '''

        # Handshake with card 
        self.get_card_uid()

        # build payload
        payload = list(databytes)

        # print friendly payload in hex
        payloadx = [hex(d) for d in payload]
        print(f"payload data = {payloadx}")

        # write the payload page by page
        payloadlength = len(payload)
        page = pagestart
        for i in range(0, payloadlength - 1, 4):
            # prepare data command
            write_command = self.get_apdu_command("Write")
            write_command[3] = page
            payload_part = payload[i:i+4]
            apdu = write_command + payload_part
            # print(f"apdu = {apdu}")
            # apdu_hex = ConvertingArrays.array_conversion(apdu, "int_to_hex")
            # print(f"apdu in hex = {apdu_hex}")

            response, sw1, sw2 = self.cardservice.connection.transmit(apdu)
            # print(f"response: {response}, sw1 = {sw1}, sw2 = {sw2}")
            if sw1 == 99:
                print(f"Failed: NFC write error sending {payload_part} at page {page}: response: {response} and status codes {sw1} and {sw2}")
                return "Failed"
            page += 1

        print(f"Success: NFC written to card: {payload}")
        return "Success"

    def send_raw_command(self, data):
        response, sw1, sw2 = self.cardservice.connection.transmit(data)
        if sw1 != 144:
            print(f"Failed sending raw command. sw1,sw2: {sw1},{sw2}")
            return "Failed"
        return bytes(response)

def convert_data_to_bytes(data):

    # Convert to bytes if necessary
    print(f"data to be written = {data}")

    if isinstance(data, str):
        databytes = bytes(data, 'utf-8')
    elif isinstance(data, list):
        databytes = bytes(data)
    elif isinstance(data, int):
        datastring = str(data)
        databytes = bytes(datastring, 'utf-8')
    else:
        databytes = data
    print(f"data converted = {databytes}")

    return databytes

# NDEFlib decoder and encoder of simple text messages
def decode_message(payload):
    """
    Returns all types of records found in the payload
    """

    print(f"NDEF payload received: {payload}")
    decoder = ndef.message_decoder(payload)

    array_of_records = list(decoder)
    print(f"NDEF records extracted: {array_of_records}")

    message = []
    for record in array_of_records:
        print(f"record type is {record.type}")
        # message += [record.text]
    print(f"Array of records found: {array_of_records}")

    return message

def decode_message_text(payload):
    """
    If you expect only a text returned from the payload
    returns all the text records found, ignoring other records
    """

    print(f"NDEF payload received: {payload}")
    decoder = ndef.message_decoder(payload)

    array_of_records = list(decoder)
    print(f"NDEF records extracted: {array_of_records}")

    message = []
    for record in array_of_records:
        message += [record.text]
    print(f"Messages found: {message}")

    return message

def encode_message_text(array_of_strings):
    """
    Receives an array of strings and returns a message that contains these in a bytearray that can be transferred to a NFC tag.
    """

    print(f"Array of strings send: {array_of_strings}")

    # create list of ndef records
    message = []
    for string in array_of_strings:
        message += [ndef.TextRecord(string)]
    print(f"NDEF Records created: {message}")

    # create ndef encoder generator
    encoder = ndef.message_encoder(message)

    # convert ndef encoder to payload octets
    payload = b''.join(encoder)
    print(f"NDEF payload created: {payload}")

    return payload 