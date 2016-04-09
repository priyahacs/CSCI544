__author__ = 'Padma'

import sys
import binascii

file = open(sys.argv[1],"rb")
outputFile = open("utf8encoder_out.txt", 'w')

byte = file.read(2)
hexi = []
count = 1
while byte != b"":
        hexi.append(byte)
        byte = file.read(2)

arr = []
for i in range(0,len(hexi)):
    hexvalue = binascii.hexlify(hexi[i])
    arr.append(hexvalue)

first = int('0x0000',16)
second = int('0x007f',16)
third = int('0x0080',16)
fourth = int('0x07ff',16)
fifth = int('0x0800',16)
sixth = int('0xffff',16)


for i in range(0,len(arr)):

    value = int(arr[i],16)
    if value >= first and value <= second:

        hex_val = "0xxxxxxx"
        binary = bin(value)[2:].zfill(7)
        hex_val = hex_val[0:1]
        hex_val = hex_val + binary
        final_char =chr(int(hex_val,2))
        outputFile.write(final_char)

    elif value >= third and value <= fourth:

        sequence1 = "110"
        sequence2 = "10"
        #binary = '{0:11b}'.format(value)
        binary = bin(value)[2:].zfill(11)
        binaryValue1 = binary[0:5]
        binaryValue2 = binary[5:11]
        sequence1 += binaryValue1
        sequence2 += binaryValue2
        final_char =chr(int(sequence1,2))+chr(int(sequence2,2))
        outputFile.write(final_char)

    elif value >= fifth and value <= sixth:

        sequence1 = "1110"
        sequence2 = "10"
        sequence3 = "10"
        binary = bin(value)[2:].zfill(16)
        binaryValue1 = binary[0:4]
        binaryValue2 = binary[4:10]
        binaryValue3 = binary[10:16]
        sequence1 += binaryValue1
        sequence2 += binaryValue2
        sequence3 += binaryValue3
        final_char = chr(int(sequence1,2))+chr(int(sequence2,2))+chr(int(sequence3,2))
        outputFile.write(final_char)

    else:
        binary = bin(value)[2:].zfill(21)
        sequence1 = "11110"
        sequence2 = "10"
        sequence3 = "10"
        sequence4 = "10"
        binaryValue1 = binary[0:3]
        binaryValue2 = binary[3:9]
        binaryValue3 = binary[9:15]
        binaryValue4 = binary[15:21]
        sequence1 += binaryValue1
        sequence2 += binaryValue2
        sequence3 += binaryValue3
        sequence4 += binaryValue4
        final_char = chr(int(sequence1,2))+chr(int(sequence2,2))+chr(int(sequence3,2))+chr(int(sequence4,2))
        outputFile.write(final_char)
