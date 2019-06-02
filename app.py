import wave, sys, os, struct, re
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
    "7": '1110111010101', "8": '111011101110101', "9": '11101110111011101', "0": '1110111011101110111',
    " ": '0000000',      "\n": '\n',               "": ''
}

inv_morse_codes = { morse : char for char, morse in morse_codes.items() }

valid_chars = list(morse_codes.keys()) #+ [' ']

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
        # para todas as linhas do arquivo
        for f_line in inp_file:
            # retira caracteres indesejados
            f_line = re.sub(' +', ' ', f_line)
            #f_line = re.sub('\n', '', f_line)
            
            last_char = ' '
            # para todos os caracteres 
            for char in f_line:
                char = char.upper()
                # se o caracter for valido, o escreve
                if char in valid_chars:
                    # se o ultimo caracter que for lido nao for um espaco entre palavras,
                    # escreve o espaco entre as letras
                    if last_char != ' ' and char != ' ':
                        output.write(SPACE_LETTERS)
                        
                    # escreve o morse equivalente
                    output.write(morse_codes[char])

                    # atuliza o ultimo char visto
                    last_char = char

            #output.write('\n')
    output.close()

def morse_to_txt(file_name):
    global inv_morse_codes
    global SPACE_WORDS
    global SPACE_LETTERS

    input_file = file_name + '.morse'
    out_file = file_name + '.txt'
    
    print("Creating file: " + out_file)
    output = open(out_file, 'w')

    with open(input_file, 'r') as inp_file:
        for f_line in inp_file:
            # retira os caracteres indesejados
            f_line = re.sub('\n', '', f_line)
            # para todas as palavras encontradas na linha
            for word in f_line.split(SPACE_WORDS):
                last_char = ''
                # para todos os caracteres na palavra
                for char in word.split(SPACE_LETTERS):
                    last_char = inv_morse_codes[char]
                    # escreve a letra correspondente
                    output.write(last_char)
                
                output.write(' ')
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
        morse = np.array([int(i) for i in inp_file.readline() if i != '\n'])
    
    num_samples = int(SAMP_RATE * TIME_UNI)

    wave_0 = [0 for i in range(num_samples)]
    wave_1 = [np.sin(2 * np.pi * FREQ * i / SAMP_RATE) for i in range(num_samples)]
    waves = [wave_0, wave_1]

    full_wave = []
    for i in morse:
        full_wave.extend(waves[i])

    plt.plot(full_wave)
    plt.savefig(file_name + '_wave.png')

    print("Creating file: " + out_file)
    print("Estimated time (in seconds): " + str(len(morse)*TIME_UNI))
    n_frames = len(full_wave)  # Len of the wave is the number of the frames.
    with wave.open(out_file, 'wb') as wave_file:
        wave_file.setparams((num_channels, sampwidth, SAMP_RATE, n_frames, comptype, compname))

        for signal in full_wave:
            value = int(signal * AMPL)
            wave_file.writeframes(struct.pack('h', value))


def wave_to_morse(file_name):
    global SAMP_RATE
    global TIME_UNI

    input_file = file_name + '.wav'
    out_file = file_name + '.morse'

    num_samples = int(SAMP_RATE * TIME_UNI)

    with wave.open(input_file, 'rb') as wave_file:
        n_frames = wave_file.getnframes()
        data = wave_file.readframes(n_frames)
        data = np.array(struct.unpack('{n}h'.format(n=n_frames), data))
        
    print('Creating file: ' + out_file) 
    output = open(out_file, 'w')
    for i in range(0, len(data), num_samples):
        if data[i:i+num_samples].max() > 0:
            output.write('1')
        else:
            output.write('0')
        
    output.close

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
            wave_to_morse(file_name)
            # morse => text
            morse_to_txt(file_name)
            return True
        else:
            print("Error: Invalid file extention!")
            return False
        

if __name__ == '__main__':
    main(sys.argv)