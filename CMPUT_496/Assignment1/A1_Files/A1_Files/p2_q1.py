import math 
import os

def extendedEclideanAlg(a, b):
    a0 = a
    b0 = b
    t0 = 0
    t = 1
    s0 = 1
    s = 0
    q = math.floor(a0//b0)
    r = a0-(q*b0)

    if b0 == 1:
        return 0

    while r > 0:

        temp = t0 - q * t
        t0 = t
        t = temp
        
        temp = s0 - (q*s)
        s0 = s
        s = temp
      
        a0 = b0
        b0 = r

        q = math.floor(a0//b0)
        r = a0-(q*b0)
    
    r = b0
    return [r,s,t]

def get_input(txt_file):
    '''Returns a and b values form a text file'''
    with open(txt_file, 'r') as f:
        input = f.readlines()

    return int(input[0].strip()), int(input[1].strip())

def output(values, file_name):
    with open(file_name, 'w') as outfile:
        for value in values:
            outfile.write(str(value) + '\n')



parentpath = os.path.join(os.getcwd(),'A1_Files','A1_Files')
a,b = get_input(os.path.join(parentpath, 'input_q1.txt'))
values = extendedEclideanAlg(a,b)
output(values,os.path.join(parentpath, 'output_q1.txt'))

