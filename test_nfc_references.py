import os
import json

import class_conversions

#imported from source, temporary
def save_json(datadict, path, filename):
    """Dumps a dictionary to a json file in the documents folder"""

    # check if directory already exists, if not create it
    if not os.path.exists(path):
        os.makedirs(path)

    filename = filename

    complete_path = os.path.join(path, filename + ".json")

    # open file and write json to it
    with open(complete_path, 'w') as savefile:
        # dump json data in the file
        json.dump(datadict, savefile, indent=4)

def load_json(path, filename):
    """Load files to the documents folder"""

    # check if directory already exists, if not create it
    if not os.path.exists(path):
        os.makedirs(path)

    complete_path = os.path.join(path, filename + ".json")

    # open save file and return the datadict
    with open(complete_path, 'r') as infile:
        datadict = json.load(infile)
    
    return datadict

if __name__ == '__main__':

    datadict = {
        "ATR (Anwser To Reset)": {
            
        },
        "Mifare Ultralight": {
            "Identify": {
                "APDU_int": [255, 202, 0, 0, 0],
                "APDU_hex": ["0XFF", "0XCA", "0X00", "0X00", "0X00"],
                "Response": {

                    }
                },
            "Read": {
                "APDU_int": [255, 176, 0, "block", 4],
                "APDU_hex": ["0XFF", "0XB0", "0X00", "block", "0X04"],
                "Response": {
                    "text": {
                        "start": {
                            "block": 6,
                            "byte": 3,
                            },
                        "end": {
                            "type": "encounter",
                            "at": 254,
                            }
                        }
                    }
                },
            "Write": {
                "APDU_int": [255, 214, 0, "block", 4],
                "APDU_hex": ["0XFF", "0XD6", "0X00", "block", "0X04"],
                "Response": {
                    "text": {
                        "start": {
                            "block": 6,
                            "byte": 3,
                            },
                        "end": {
                            "type": "encounter",
                            "at": 254,
                            }
                        }
                    }
                }
            }
        }

    # print(class_conversions.ConvertingNumbers.hex_to_int("0XD6"))
    save_json(datadict, os.path.join("lib", "python_nfc_lib", "references"), "nfc_communication")