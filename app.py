import wave, sys
import numpy as np

# --------------------------------------------------------------------------------------------- Global Variables
morse_codes = {
    "A": '10111',         "B": '111010101',       "C": '11101011101',       "D": '1110101',
    "E": '1',             "F": '101011101',       "G": '111011101',         "H": '1010101',
    "I": '101',           "J": '1011101110111',   "K": '111010111',         "L": '101110101',
    "M": '1110111',       "N": '11101',           "O": '11101110111',       "P": '10111011101',
    "Q": '1110111010111', "R": '1011101',         "S": '10101',             "T": '111',
    "U": '1010111',       "V": '101010111',       "W": '101110111',         "X": '11101010111',
    "Y": '1110101110111', "Z": '11101110101',     "1": '10111011101110111', "2": '101011101110111',
    "3": '1010101110111', "4": '10101010111',     "5": '101010101',         "6": '11101010101',
    "7": '1110111010101', "8": '111011101110101', "9": '11101110111011101', "0": '1110111011101110111',
    " ": '0000000'
}

invert_morse_codes = { morse : char for char, morse in morse_codes.items() }

valid_chars = list(morse_codes.keys())

SPACE = '000'

# -------------------------------------------------------------------------------------------- Functions
def text_to_morse(input_file):
    global morse_codes
    global valid_chars
    out_file = input_file.split('.txt')[0] + '.morse'
    
    print("Creating file: " + out_file)
    output = open(out_file, 'w')

    

    with open(input_file, 'r') as inp_file:
        break_point = False

        while not break_point:
            char = inp_file.read(1)

            if not char:
                break_point = True
            elif char in valid_chars:
                output.write(morse_codes[char.upper()])
                
                if char != ' ':
                    output.write(SPACE)

    

    output.close()



# ------------------------------------------------------------------------------------------- Main
def main(args):
    if(len(args) < 2):
        print("Error: Input file expected.")
        return False
    else:
        input_file = args[1]
        print("Input File: " + input_file)

        if input_file.endswith('.txt'):
            # text => morse
            text_to_morse(input_file)
            # text => wav OU morse => wave
            return True
        elif input_file.endswith('.morse'):
            # morse => text
            # morse => wav
            return True
        elif input_file.endswith('.wav'):
            # wav => text
            # wav => morse OU text => morse
            return True
        else:
            print("Error: Invalid file extention!")
            return False
        

if __name__ == '__main__':
    main(sys.argv)