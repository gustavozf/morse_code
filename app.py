import wave, sys, os, struct
import numpy as np

import matplotlib.pyplot as plt

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
    "7": '1110111010101', "8": '111011101110101', "9": '11101110111011101', "0": '1110111011101110111'
}

inv_morse_codes = { morse : char for char, morse in morse_codes.items() }

valid_chars = list(morse_codes.keys()) + [' ']

SPACE_LETTERS = '000'
SPACE_WORDS = '0000000'

# Frequência como constante 440 hz;
FREQ = 440
    
# Taxa de amostragem constante 48000;
SAMP_RATE = 48000

# Amplitude 16000;
AMPL = 16000

#Unidade de tempo de som como constante com valor de 0.25s. 
#Isto é, uma unidade do código morse dura 0.25s, tratar uma pequena variação disso se for necessário, +- 0.01s;
TIME_UNI = 0.25

# -------------------------------------------------------------------------------------------- Functions
def text_to_morse(file_name):
    global morse_codes
    global valid_chars

    input_file = file_name + '.txt'
    out_file = file_name + '.morse'

    print("Creating file: " + out_file)
    output = open(out_file, 'w')

    with open(input_file, 'r') as inp_file:
        break_point = False
        put_space = False

        # read the file char by char
        while not break_point:
            char = inp_file.read(1).upper()

            # if EOF
            if not char:
                break_point = True
            # else, if the read char is valid
            elif char in valid_chars:
                if char == ' ':
                    put_space = True
                else:
                    if(put_space):
                        output.write(SPACE_WORDS)
                        put_space = False

                    output.write(morse_codes[char])
                    output.write(SPACE_LETTERS)
             
    output.close()

def morse_to_txt(file_name):
    global inv_morse_codes

    input_file = file_name + '.morse'
    out_file = file_name + '.txt'
    
    print("Creating file: " + out_file)
    output = open(out_file, 'w')

    with open(input_file, 'r') as inp_file:
        break_point = False
        zeros_count = 0
        morse_word = ''

        while not break_point:
            char = inp_file.read(1)

            if not char:
                output.write(inv_morse_codes[morse_word[:-zeros_count]])
                #print("'{}' : {}".format(morse_word[:-zeros_count], inv_morse_codes[morse_word[:-zeros_count]]))
                
                break_point = True
            elif char == '0':
                zeros_count += 1
            else:
                if zeros_count >= 3:
                    output.write(inv_morse_codes[morse_word[:-zeros_count]])
                    #print("'{}' : {}".format(morse_word[:-zeros_count], inv_morse_codes[morse_word[:-zeros_count]]))
                    morse_word = ''

                    if zeros_count > 4:
                        output.write(' ')
                        #print("'{}' : '{}'".format('0000000', ' '))
                zeros_count = 0

            morse_word += char
                
    output.close()


def morse_to_wave(file_name):
    global FREQ
    global AMPL
    global SAMP_RATE
    global TIME_UNI

    input_file = file_name + '.morse'
    out_file = file_name + '.wav'

    comptype='NONE'
    compname='not compressed' 
    sampwidth=2
    num_channels=1

    with open(input_file, 'r') as inp_file:
        morse = np.array([int(i) for i in inp_file.readline()])
    
    num_samples = int(SAMP_RATE * TIME_UNI)

    wave_0 = [0 for i in range(num_samples)]
    wave_1 = [np.sin(2 * np.pi * FREQ * i / SAMP_RATE) for i in range(num_samples)]
    waves = [wave_0, wave_1]

    full_wave = []
    for i in morse:
        full_wave.extend(waves[i])

    plt.plot(full_wave)
    plt.savefig(file_name + '_wave.pdf')

    print("Creating file: " + out_file)
    n_frames = len(full_wave)  # Len of the wave is the number of the frames.
    with wave.open(out_file, 'w') as wave_file:
        wave_file.setparams((num_channels, sampwidth, SAMP_RATE, n_frames, comptype, compname))

        for signal in full_wave:
            value = int(signal * AMPL)
            wave_file.writeframes(struct.pack('h', value))


def wave_to_morse(input_file):
    pass

# ------------------------------------------------------------------------------------------- Main
def main(args):
    if(len(args) < 2):
        print("Error: Input file expected.")
        return False
    else:
        input_file = args[1]
        print("Input File: " + input_file)

        if not os.path.isfile(input_file):
            print("Error: File not found!")
            return False

        if input_file.endswith('.txt'):
            file_name = input_file.split('.txt')[0]
            # text => morse
            text_to_morse(file_name)
            # morse => wave
            morse_to_wave(file_name)

            return True
        elif input_file.endswith('.morse'):
            file_name = input_file.split('.morse')[0]
            # morse => text
            morse_to_txt(file_name)
            # morse => wav
            morse_to_wave(file_name)

            return True
        elif input_file.endswith('.wav'):
            file_name = input_file.split('.wav')[0]
            # wav => morse 
            # morse => text
            morse_to_txt(file_name)
            return True
        else:
            print("Error: Invalid file extention!")
            return False
        

if __name__ == '__main__':
    main(sys.argv)