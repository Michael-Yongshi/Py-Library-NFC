import os
import json

class NFCreference(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_reference_material():

        # # set the paths to the apdu reference file
        # path = os.path.join(os.path.dirname(__file__)) # the same folder as caller
        # filename = "nfc_communication"
        # complete_path = os.path.join(path, filename + ".json")

        # # open file and return the dictionary
        # with open(complete_path, 'r') as infile:
        #     datadict = json.load(infile)
        
        # print(datadict)
        # return datadict

        datadict = {'ATR (Anwser To Reset)': {'start byte': {'start': 0, 'end': 1}, 'historical byte count': {'start': 1, 'end': 2}, 'length': {'start': 6, 'end': 7}, 'Registered App Provider Identifiers (RIDs)': {'start': 7, 'end': 12, 'Known values': {'PC/SC Workgroup': ['0xa0', '0x0', '0x0', '0x3', '0x6'], '': ''}}, 'Standards': {'start': 12, 'end': 13, 'Known values': {'ISO14443A, Part3': ['0x3'], '': ''}}, 'Card Types': {'start': 13, 'end': 15, 'Known values': {'Mifare 1K': ['0x0', '0x1'], 'Mifare 4k': ['0x0', '0x2'], 'Mifare Ultralight': ['0x0', '0x3'], 'Mifare Mini': ['0x0', '0x26'], 'Topaz and Jewel': ['0xF0', '0x4'], 'Felica 212k': ['0xF0', '0x11'], 'Felica 424k': ['0xF0', '0x12']}}, 'Radio Frequency Units (RFUs)': {'start': 15, 'end': 19, 'Known values': {'Default setting': ['0x0', '0x0', '0x0', '0x0'], '': ''}}}, 'Mifare Ultralight': {'Identify': {'APDU_int': [255, 202, 0, 0, 0], 'APDU_hex': ['0xFF', '0xCA', '0x0', '0x0', '0x0'], 'Response': {}}, 'Read': {'APDU_int': [255, 176, 0, 'block', 4], 'APDU_hex': ['0xFF', '0xB0', '0x0', 'block', '0x4'], 'Response': {'text': {'start': {'block': 6, 'byte': 3}, 'end': {'type': 'encounter', 'at': 254}}}}, 'Write': {'APDU_int': [255, 214, 0, 'block', 4], 'APDU_hex': ['0xFF', '0xD6', '0x0', 'block', '0x4'], 'Response': {'text': {'start': {'block': 6, 'byte': 3}, 'end': {'type': 'encounter', 'at': 254}}}}}}

        # print(datadict)
        return datadict