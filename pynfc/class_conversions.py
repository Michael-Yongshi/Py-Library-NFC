
# converting numbers (number to different base number)
# encoding characters (char to number)
# decoding characters (number to char)

class ConvertingArrays(object):
    """dynamically set up a method to call conversions for arrays"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def array_conversion(dataarray, conversion):
        """convert a whole array"""

        i_new = "not set"
        dataarray_new = []
        for i in dataarray:
            if conversion == "int_to_bit": i_new = ConvertingNumbers.int_to_bit(i) 
            if conversion == "int_to_oct": i_new = ConvertingNumbers.int_to_oct(i)
            if conversion == "int_to_hex": i_new = ConvertingNumbers.int_to_hex(i)
            
            if conversion == "bit_to_int": i_new = ConvertingNumbers.bit_to_int(i) 
            if conversion == "bit_to_oct": i_new = ConvertingNumbers.bit_to_oct(i) 
            if conversion == "bit_to_hex": i_new = ConvertingNumbers.bit_to_hex(i) 

            if conversion == "hex_to_bit": i_new = ConvertingNumbers.hex_to_bit(i) 
            if conversion == "hex_to_int": i_new = ConvertingNumbers.hex_to_int(i) 
            if conversion == "hex_to_oct": i_new = ConvertingNumbers.hex_to_oct(i) 
            if conversion == "hex_to_hexstr": i_new = ConvertingNumbers.hex_to_hexstr(i)
            dataarray_new += [i_new]

        return dataarray_new

class ConvertingNumbers(object):
    """
    integers are the normally known digits with 10 numbers (0-9), also known as numbers with base 10. 
    These can be converted to numbers with other bases, like base 2 (bits; 0-1) or base 16 (hexadecimals; 0-9 + a-f).
    i.e. the number 65 with base 10 (so our normal numbering like we humans understand it) is expressed:
     - in integers its          65                  (6*10 + 5*1)
     - in bit like             (0b)1000001          (1*64 + 0*32 + 0*16 + 0*8 + 0*4 + 0*2 + 1*1)
     - in hex like              (0x)41(h)           (4*16 + 1*1)
    These are basically all the same thing except written down in a different format.
    To let people and programs know in what base the number is supposed to be read, a prefix (or postfix) is often used, represented in the above table within brackets.
    Exception for base 10, because we are used to read the number 65 in our decimal system, as it is for us our default base, it is in encoding the same. 
    the number 0x65 or 65h is actually the number 101 in our decimal / base 10 system

    methods with example integer 65 as we humans know it:
    - int_to_bit        65              ->      (0b)1000001
    - int_to_oct        65              ->      (0o)81
    - int_to_hex        65              ->      (0x)41(h)
    
    - bit_to_int       (0b)1000001     ->      65
    - bit_to_oct       (0b)1000001     ->      (0o)81
    - bit_to_hex       (0b)1000001     ->      (0x)41(h)

    - hex_to_bit       (0x)41(h)       ->      (0b)1000001
    - hex_to_int       (0x)41(h)       ->      65
    - hex_to_oct       (0x)41(h)       ->      (0o)81
    - hex_to_hexstr    (0x)41(h)       ->      "41"
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def int_to_bit(integer):
        """convert integer to a string of bits (a number of 2 characters, 0 and 1)"""

        int_to_bit = bin(integer)
        return int_to_bit

    @staticmethod
    def int_to_oct(integer):
        """convert the integer to a string of octodecimals (a number of 18 characters, 0 to 8)"""
        
        int_to_oct = oct(integer)
        return int_to_oct

    @staticmethod
    def int_to_hex(integer):
        """convert the integer to a string of hexadecimals (a number of 16 characters, 0 to 9 and a - f)"""
        
        int_to_hex = hex(integer) # or we could use chr(integer)
        return int_to_hex

    @staticmethod
    def bit_to_int(bit):
        """convert bit into an integer"""

        bit_to_int = int(bit, 2)
        return bit_to_int

    @staticmethod
    def bit_to_oct(bit):
        """in order for a bit to oct conversion, we could just transform bits to integers and those integers to octs"""
        
        bit_to_int = ConvertingNumbers.bit_to_int(bit)
        int_to_oct = ConvertingNumbers.int_to_oct(bit_to_int) 
        return int_to_oct

    @staticmethod
    def bit_to_hex(bit):
        """in order for a bit to hex conversion, we could just transform bits to integers and those integers to hexes"""
        
        bit_to_int = ConvertingNumbers.bit_to_int(bit)
        int_to_hex = ConvertingNumbers.int_to_hex(bit_to_int) 
        return int_to_hex

    @staticmethod
    def oct_to_bit(octodecimal):
        """in order for a oct to bit conversion, we could just transform oct to integers and those integers to bits"""
        
        oct_to_int = ConvertingNumbers.oct_to_int(octodecimal)
        int_to_bit = ConvertingNumbers.int_to_bit(oct_to_int) 
        return int_to_bit

    @staticmethod
    def oct_to_int(octodecimal):
        """convert the octodecimal to an integer
        python uses the int command to convert octodecimals (base 16) to a normal integer (base 10)"""
        
        oct_to_int = int(octodecimal, 8)
        return oct_to_int

    @staticmethod
    def oct_to_hex(octodecimal):
        """in order for a oct to hex conversion, we could just transform oct to integers and those integers to hexes"""
        
        oct_to_int = ConvertingNumbers.oct_to_int(octodecimal)
        int_to_hex = ConvertingNumbers.int_to_hex(oct_to_int) 
        return int_to_hex

    @staticmethod
    def hex_to_bit(hexadecimal):
        """in order for a hex to bit conversion, we could just transform hex to integers and those integers to bits"""
        
        hex_to_int = ConvertingNumbers.hex_to_int(hexadecimal)
        int_to_hex = ConvertingNumbers.int_to_hex(hex_to_int) 
        return int_to_hex

    @staticmethod
    def hex_to_int(hexadecimal):
        """convert the hexadecimal to an integer
        python uses the int command to convert hexadecimals (base 16) to a normal integer (base 10)"""
        
        hex_to_int = int(hexadecimal, 16)
        return hex_to_int

    @staticmethod
    def hex_to_oct(hexadecimal):
        """in order for a hex to oct conversion, we could just transform hex to integers and those integers to octs"""
        
        hex_to_int = ConvertingNumbers.hex_to_int(hexadecimal)
        int_to_oct = ConvertingNumbers.int_to_oct(hex_to_int) 
        return int_to_oct
    
    @staticmethod
    def hex_to_hexstr(hexadecimal):
        """strip the hex values of their prefix"""
        
        hex_to_hexstr = hexadecimal[2:] if len(hexadecimal) == 4 else f"0{hexadecimal[2:]}"
        return hex_to_hexstr

class EncodingCharacter(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def character_to_integer(string):
        """
        However integers and other numbers are sometimes used to represent characters also, like the ascii or unicode standard. Unlike converting numbers to numbers with a different base,
        which is all mathematically simple, characters have no inherent base or association to a number, as we just made them up and arranged them arbitrarily in an order
        (the so called alfabet in western countries). For this we need a standard, and often the ascii or unicode standards are used.
        Ascii and unicode have normal latin characters start at A-65 to Z-90 and a-97 to z-122
        However they can also have a unicode code point, which uses hexadecimal digits, instead of an integer (base10) representing a character,
        a hexadecimal (base16) can also be used to represent a character.
        So our first letter of the alfabet A could be converted to:
        - its unicode integer          65
        - its unicode code point       (U)0041
        """
        integer = ord(string)
        return integer

    @staticmethod
    def character_to_unicode_codepoint(string):
        """ unicode codepoint is basically the hexadecimal version of the representation of a character.
        So character 'A' is represented in integer as 65, unicode codepoint is just this integer written in hexadecimals (so 41)"""
        integer = EncodingCharacter.character_to_integer(string)
        unicode_codepoint = ConvertingNumbers.int_to_hex(integer)
        return unicode_codepoint

class DecodingCharacter(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def integer_to_character(integer):
        """
        converting an integer value to a unicode / ascii value. Unicode is a superset of ascii, where ascii comprises over the numbers 1 - 127 (or 255 in the extended)
        unicode doesnt have a limit. 
        """

        int_to_character = chr(integer)
        return int_to_character

    @staticmethod
    def unicode_codepoint_to_character(unicode_codepoint):
        """most used characters in unicode can be represented within a 4 byte code point, represented by U0000 (u is a prefix so we know its unicode) 
        where the digits are hexadecimal (0-9,a-f). so the amount of character in this format is 16 to the power of 4 is more than 65000 combinations (integers 1-65000). 
        thus unicode can be written down as an integer: 65 is letter A and as a code point: U0041 (the 4 represents 4*16, + another 1 makes 65)"""
        
        integer = ConvertingNumbers.hex_to_int(unicode_codepoint)
        int_to_character = chr(integer)
        return int_to_character


if __name__ == '__main__':

    string = "A"

    integer = EncodingCharacter.character_to_integer(string)
    print(f"Encode A to integer: {integer}")
    string = DecodingCharacter.integer_to_character(integer)
    print(f"Decode A from integer: {string}")

    unicode_codepoint = EncodingCharacter.character_to_unicode_codepoint(string)
    print(f"Encode A to unicode code point: {unicode_codepoint}")
    string = DecodingCharacter.unicode_codepoint_to_character(unicode_codepoint)
    print(f"Decode A from unicode code point: {string}")