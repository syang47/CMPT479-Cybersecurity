import sys
import math

def hamming_code(string):
    # Handle input string
    byte_string = bytes(string, "utf8")
    bit_string = ''
    for x in byte_string:
        bit_string = bit_string + "{:08b}".format(x)

    # Find number of parity bits
    binary = list(bit_string)
    bit_length = len(binary)
    parity_num = math.floor(math.log2(bit_length + 1) + 1)

    # Calculate for parity
    for i in range(parity_num):
        binary.insert(2**i -1,'0')
    bit_length = len(binary)
    
    # Find parity of input string with M
    p = []
    for i in range(parity_num):
        count = 2**i
        pos = 2**i - 1
        result = 0
        
        while pos < bit_length:
            count -= 1
            result = int(binary[pos]) ^ int(result)
            pos += 1
            
            if count == 0:
                count = 2**i
                pos += 2**i
                
        p.append(str(result))
    return p

string = sys.argv[1]
result = hamming_code(string)
print(''.join(result))

