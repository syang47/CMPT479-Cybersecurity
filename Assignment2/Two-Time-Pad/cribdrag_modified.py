# screen changed
def xor(a, b):
    #input: two byearrays
    #output: bytearray of their xor
    if len(a) > len(b):
        temp = a
        a = b
        b = temp
    s = []
    for i in range(0, len(a)):
        s.append(a[i] ^ b[i])
    for i in range(len(a), len(b)):
        s.append(b[i])
    return s

def cribpend(a, crib, loc):
    #crib is too small; append it with 0's depending on location
    s = []
    for i in range(0, loc):
        s.append(0)
    for i in range(0, len(crib)):
        s.append(crib[i])
    for i in range(len(crib) + loc, len(a)):
        s.append(0)
    s = s[:len(a)]
    return s

def bit(a):
    #returns bitstring of integer
    s = ""
    while (a != 0):
        if (a % 2 == 0):
            s += "0"
            a /= 2
        else:
            s += "1"
            a -= 1
            a /= 2
    while len(s) < 8:
        s += "0"
    s = s[::-1]
    return s

def s_to_ints(s):
    #convert string to integer list ("bytearray")
    b = []
    for i in range(0, len(s)):
        b.append(ord(s[i]))
    return b
    

def showbytes(a):
    s = ""
    chars = []
    for i in range(65, 91):
        chars.append(i)
    for i in range(97, 123):
        chars.append(i)
    for i in range(44, 47):
        chars.append(i)
    #return string of bytestring
    for i in range(0, len(a)):
        if (a[i] in chars):
            s += chr(a[i])
        elif (a[i] == 0):
            s += " "
        elif (a[i] == 32):
            s += "_"
        else:
            s += "*"
    return s

import pygame
import random
import sys

is_blue = 1
done = 0
x = 30
y = 30
clock = pygame.time.Clock()
# 
# p1s = "Seven for the Dwarf-lords in halls of stone."
# p2s = "In the land of Mordor where the shadows lie."

#our byte arrays are just integer lists
# p1 = s_to_ints(p1s)
# p2 = s_to_ints(p2s)
#generate
# k = []
# for i in range(0, len(p1s)):
#     k.append(random.randint(0, 255))
    
f0 = open('ctext0', 'rb')
f1 = open('ctext1', 'rb')
# 
# c1 = xor(p1, k)
# c2 = xor(p2, k)

c3 = f0.read(600)
c4 = f1.read(600)


c3_01 = c3[:100]
c3_02 = c3[100:200]
c3_03 = c3[200:300]
c3_04 = c3[300:400]
c3_05 = c3[400:500]
c3_06 = c3[500:600]

c4_01 = c4[:100]
c4_02 = c4[100:200]
c4_03 = c4[200:300]
c4_04 = c4[300:400]
c4_05 = c4[400:500]
c4_06 = c4[500:600]

# just modify this number to display different portion of our cipher texts
chunk = 0
if chunk == 1:
    c3 = c3_02
    c4 = c4_02
elif chunk == 2:
    c3 = c3_03
    c4 = c4_03
elif chunk == 3:
    c3 = c3_04
    c4 = c4_04
elif chunk == 4:
    c3 = c3_05
    c4 = c4_05
elif chunk == 5:
    c3 = c3_06
    c4 = c4_06
else:
    c3 = c3_01
    c4 = c4_01

x = xor(c3, c4)

pygame.init()
screen = pygame.display.set_mode((1200, 700))
screen.fill((255, 255, 255))
pygame.display.flip()

r = []
is_cap = 0
is_drag = 0
inputting = 0
loc = 0
towrite = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0] >= 200 and event.pos[0] <= 1000 and event.pos[1] >= 400 and event.pos[1] <= 425):
                is_drag = 1
                #start dragging
                
        if event.type == pygame.MOUSEMOTION and is_drag == 1:
            loc = int((event.pos[0] - 200) / 8)
            if (loc < 0):
                loc = 0
            if (loc > 99):
                loc = 99
                
        if event.type == pygame.MOUSEBUTTONUP:
            is_drag = 0
            if (event.pos[0] >= 200 and event.pos[1] >= 400 and event.pos[1] <= 425):
                #override the rest; we don't want to change output
                continue
            charnum = int((event.pos[0] - 200)/8)
            lineremain = event.pos[1] % 100
            linenum = int((event.pos[1] - 100) / 100)
            if (charnum >= 0 and charnum <= 99 and (lineremain <= 35 or lineremain >= 90) and linenum >= 0 and linenum <= 4):
                towrite = 1
            else:
                towrite = 0
                
        if event.type == pygame.KEYDOWN and inputting == 1:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                inputting = 0
                print("we are no longer inputting")
                continue
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                is_cap = 1
            elif event.key == pygame.K_BACKSPACE and len(r) > 0:
                if (is_cap == 1):
                    # delete faster, 5 chars in one time
                    r = r[:-5]
                else:
                    r = r[:-1]
            else:
                try:
                    this_r = int(event.key)
                    if (is_cap == 1):
                        if (this_r == 61):
                            this_r -= 18
                        elif (this_r == 55 or this_r == 57 or this_r == 48):
                            this_r -= 17
                        elif (this_r == 49 or this_r == 51 or this_r == 52 or this_r == 53):
                            this_r -= 16
                        elif (this_r == 56):
                            this_r -= 14
                        elif (this_r == 39):
                            this_r -= 5
                        elif (this_r == 59):
                            this_r -= 1
                        elif (this_r == 50):
                            this_r += 14
                        elif (this_r == 44 or this_r == 46 or this_r == 47):
                            this_r += 16
                        elif (this_r == 96):
                            this_r += 30
                        elif (this_r == 92 or this_r == 93 or this_r == 91):
                            this_r += 32
                        elif (this_r == 45 or this_r ==54):
                            this_r += 50
                        else:
                            this_r = max(0, this_r - 32)
                    r.append(this_r)
                except:
                    pass
                
        if event.type == pygame.KEYDOWN and inputting == 0:
            if (event.key == pygame.K_RETURN):
                inputting = 1
                print("we are now inputting")
                
        if event.type == pygame.KEYUP and inputting == 1:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                is_cap = 0
    keys = pygame.key.get_pressed()
##    if keys[pygame.K_BACKSPACE] and len(r) > 0 and inputting == 1:
##        r = r[:-1]
##        clock.tick(15)
            
    screen.fill((255, 255, 255))
    
    myfont = pygame.font.SysFont("Arial", 22, bold=True)
    label = myfont.render("COMP3632 Crib-dragging part " + str(chunk), 1, (0, 0, 0))
    screen.blit(label, (15, 15))
    
    myfont = pygame.font.SysFont("Arial", 22, italic=True)
    label = myfont.render("Ciphertext 1 (C1):", 1, (0, 125, 0))
    screen.blit(label, (50, 50))
    
    label = myfont.render("Ciphertext 2 (C2):", 1, (0, 125, 0))
    screen.blit(label, (50, 150))
    
    label = myfont.render("Xortext (X = C1 XOR C2):", 1, (0, 125, 0))
    screen.blit(label, (50, 250))
    
    label = myfont.render("Crib (R):", 1, (255, 0, 0))
    screen.blit(label, (50, 350))
    
    label = myfont.render("Xorcribtext (X XOR R):", 1, (0, 125, 0))
    screen.blit(label, (50, 450))
    
    
    myfont = pygame.font.SysFont("monospace", 14)
    # font 14 means 8 px wide and 17 px high
    label = myfont.render(showbytes(c3), 1, (0, 0, 0))
    screen.blit(label, (202, 100))
#     print('width: ', label.get_width())
#     print('height: ', label.get_height())
    
    label = myfont.render(showbytes(c4), 1, (0, 0, 0))
    screen.blit(label, (202, 200))
    
    label = myfont.render(showbytes(x), 1, (0, 0, 0))
    screen.blit(label, (202, 300))
    
    rp = cribpend(c3, r, loc) #r, appended
    
    label = myfont.render(showbytes(rp), 1, (255, 0, 0))
    screen.blit(label, (202, 400))
    
    xr = xor(x, rp)
    
    label = myfont.render(showbytes(xr), 1, (0, 0, 0))
    screen.blit(label, (202, 500))
    
    myfont = pygame.font.SysFont("Arial", 8)
    for j in range(0, 5):
        tx = 200
        ty = 100
        width = 800
        height = 17
        pygame.draw.polygon(screen, (0, 235, 235),
                            ((tx, ty+j*100), (tx+width, ty+j*100),
                             (tx+width, ty+height+j*100), (tx, ty+height+j*100)),
                            2)
    if (inputting == 1):
        # when inputting, change the rectangle of R to red
        j = 3
        pygame.draw.polygon(screen, (255, 0, 0),
                            ((tx, ty+j*100), (tx+width, ty+j*100),
                             (tx+width, ty+height+j*100), (tx, ty+height+j*100)),
                            2)
        # here we draw the 'cursor'
        pygame.draw.line(screen, (255, 0, 0),
                         (202+(loc+len(r))*8, 400), (202+(loc+len(r))*8, 417)
                         )
    for j in range(0, 5):
        for i in range(0, 100):
            label = myfont.render(str(i), 1, (150, 150, 150))
            screen.blit(label, (200 + i * 8 + 4, 80 + j * 100))
    if (towrite == 1):
        vnames = ["C1", "C2", "Xortext", "R", "Xorcribtext"]
        vname = vnames[linenum]
        vs = [c3, c4, x, rp, xr]
#         print("charnum: ", charnum)
#         print('vs(len): ', len(vs))
#         print('vs[0](len): ', len(vs[0]))
        vstr = str(vs[linenum][charnum])
        
        vstr += str(" (" + bit(vs[linenum][charnum]) + ")")
        
        myfont = pygame.font.SysFont("Arial", 18)
        label = myfont.render("Char " + str(charnum) + " of " + vname + ": " + vstr, 1, (0, 0, 0))
        screen.blit(label, (100, 600))
        
        if linenum == 2:
            s = "C1[{}] XOR C2[{}] = {}({}) XOR {}({}) = {}({})".format(
                charnum, charnum,
                c3[charnum], bit(c3[charnum]),
                c4[charnum], bit(c4[charnum]),
                x[charnum], bit(x[charnum]))
            label = myfont.render(s, 1, (135, 0, 0))
            screen.blit(label, (100, 630))
            
        if linenum == 4:
            s = "X[{}] XOR R[{}] = {}({}) XOR {}({}) = {}({})".format(
                charnum, charnum,
                x[charnum], bit(x[charnum]),
                rp[charnum], bit(rp[charnum]),
                xr[charnum], bit(xr[charnum]))
            label = myfont.render(s, 1, (135, 0, 0))
            screen.blit(label, (100, 630))
    pygame.display.flip()
    clock.tick(30)
            

#while not done:
#        for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                        done = True
#                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                        is_blue = not is_blue
#        
#        pressed = pygame.key.get_pressed()
#        if pressed[pygame.K_UP]: y -= 3
#        if pressed[pygame.K_DOWN]: y += 3
#        if pressed[pygame.K_LEFT]: x -= 3
#        if pressed[pygame.K_RIGHT]: x += 3
#        
#        if is_blue: color = (0, 128, 255)
#        else: color = (255, 100, 0)
#        screen.fill((0, 0, 0))
#        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
#
#        pygame.display.flip()
#        clock.tick(60)
