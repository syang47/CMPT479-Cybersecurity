from random import randint
import subprocess
import sys
import math
import copy

from sqlalchemy import null

def decrypt_byte(y, n, ind, decrypt_block):

    # Generate a random block r with 15 random bytes.
    r_block = bytearray()
    for i in range(0, 16):
        r_block.append(randint(0, 255))
    r_block[ind - 1] = 0
    
    for i in range(ind, 16):
        xor = decrypt_block[i] ^ (ind-1)
        r_block[i] = xor
    
    # Ask the padding oracle if (r|y_n) is valid
    output = 0
    valid = r_block + y[n-1]
    while not output:
        f = open("blockByte", "wb")
        f.write(valid)
        f.close()
        # Checking with padding oracle.
        output = int(subprocess.check_output(['python3', 'oracle.py', 'blockByte']))
        # if oracle returned yes.
        if output:      
            break
        valid[ind - 1] += 1
    i = valid[ind - 1]
    
    if ind == 16:   # y needs to be at 16 bytes
        k = 1
        while k < (ind - 1):    # if the new (r|y_n) has valid padding
            # replacing r
            valid[k-1] = randint(0,255)
            f = open("blockByte", "wb")
            f.write(valid)
            f.close()
            output = int(subprocess.check_output(['python3', 'oracle.py', 'blockByte']))

            # if no valid padding (finished replacing) break the loop
            if not output:
                break
            k += 1
        if k == 15:     # if oracle returned yes then D(y_n) = i XOR 15
            d_fcn = i ^ 15
        else:       # if the oracle returned no then D(y_n) = i XOR k-1
            d_fcn = i ^ (k-1)
        return d_fcn
    else:
        k = ind
        d_fcn = i ^ (k-1)
        return d_fcn


# Returns a byte string
def byteString(a):
    s = ""
    for i in range(0, len(a)):
        s += chr(a[i])
    return s

def check_padding(y):
    blk = int(math.floor(len(y)/16))
    # print(blk)
    # print(len(y))
    padnum = (blk*16-len(y) ) if (blk*16-len(y)) > 0 else 16
    # print(padnum)
    y = y + bytes([padnum]) * padnum
    return y
    
if __name__ == '__main__' :

    y = open(sys.argv[1], "rb")
    y = check_padding(y.read())


    n = len(y) // 16
    y = [y[i:i+16] for i in range(0, len(y), 16)]
    r_block = [bytearray([randint(0, 255) for i in range(0, 16)])]
    temp = copy.deepcopy(r_block)

    n_chars = r_block
    chars = []
    for j in range(n,0,-1):

        decrypt_block = [0 for i in range(0,16)]

        for k in range(16,0,-1):
            decrypt_block[k-1] = decrypt_byte(n_chars, 1, k, decrypt_block)

        for k in range(0,16):
            n_chars[0][k] = decrypt_block[k] ^ y[j-1][k]

        temp2 = copy.deepcopy(n_chars[0])
        chars.insert(0, temp2)

    chars.append(temp[0])
    f = open("encrypt_result", "wb")
    for k in chars:
        f.write(k)
    f.close()


