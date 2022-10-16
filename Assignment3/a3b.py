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
    return p, parity_num, bit_string

input_parity = sys.argv[1]
input_string = sys.argv[2]
result, parity_num, bit_string = hamming_code(input_string)
correct_string = ''

# create xor list
l1 = list(result)
l2 = list(input_parity)
xor = [0 for i in range(len(result))]
for i in range(len(result)):
    xor[i] = int(l1[i]) ^ int(l2[i])

cond = sum(xor)
if(cond <= 1):
    if(cond == 0):
        parity_list = input_parity
        correct_string = input_string
    if(cond == 1):
        parity_list = list(input_parity)
        bit_string_f = input_string
        for i in range(parity_num):
            if xor[i] == 1:
                if input_parity[i] == '0':
                    parity_list[i] = '1'  
                else: 
                    parity_list[i] = '0'
        parity_list = "".join(parity_list)
        correct_string = input_string
else:
    bit_string_f = ''
    binIndex = ['0'] * parity_num
    for i in range(parity_num):
        if xor[i] == 1:
            binIndex[-1*(i+1)] ='1'
    index = int(''.join(binIndex), 2)
    
    for i in range(1, parity_num + 1):
        insert = input_parity[i-1]
        pos = 2**(i-1)-1
        bit_string = bit_string[0: pos] + insert + bit_string[pos:]

    ham_list = list(bit_string)
    if ham_list[index-1] == '0': 
        ham_list[index-1] = '1' 
    else:
        ham_list[index-1] = '0'
    
    for i in range(1,len(ham_list)+1):
        if (i & (i - 1)) == 0:
            continue
        bit_string_f += ham_list[i-1]

    parity_list = input_parity
    for i in range(0,len(bit_string_f),8):
        correct_string += chr(int(bit_string_f[i:i+8],2))
    
print(parity_list)
print(correct_string)