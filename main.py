import numpy as np
from PIL import Image
import heapq
import pickle

# read an image
image_url = "four.png"
image = Image.open(image_url)
array = np.array(image)

# array = np.array([[(1, 2), (3, 4), (5, 6)], [(1, 2), (3, 4), (5, 6)], [(1, 2), (3, 4), (5, 6)]])


# add secret message




# initializing frequency table
frequency_table = {}
for row in array:
    for element in row:
        frequency_table[tuple(element)] = 0

for row in array:
    for element in row:
        frequency_table[tuple(element)] += 1


# huffman coding
class Node():
    freq: int
    symbol: tuple

    def __init__(self, freq, symbol = (), left = None, right = None) -> None:
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.symbol}: {self.freq}'

    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def __gt__(self, other) -> bool:
        return self.freq > other.freq

    def __le__(self, other) -> bool:
        return self.freq < other.freq

    def __ge__(self, other) -> bool:
        return self.freq >= other.freq


heap: list[Node] = [Node(frequency_table[key], key) for key in frequency_table]


heapq.heapify(heap)
while len(heap) > 1:
    left: Node = heapq.heappop(heap)
    right: Node = heapq.heappop(heap)

    heapq.heappush(heap, Node(left.freq+right.freq, (), left, right))

root = heap[0]
decode = {}

def traverse(n: Node, s: str):
    if n.left is None:
        decode[n.symbol] = s
        return
    traverse(n.left, s+'0')
    traverse(n.right, s+'1')

traverse(root, '')
height, width, depth = array.shape


# writing key to file
with open("key.pickle", 'wb') as f:
    decode['height'] = height
    decode['width'] = width
    decode['depth'] = depth
    pickle.dump(decode,f)


binary_string = ''
for row in range(array.shape[0]):
    for col in range(array.shape[1]):
        binary_string += decode[tuple(array[row][col])]

if len(binary_string) % 8 != 0:
    binary_string += '0' * (len(binary_string) % 8)


bit_string = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]


#f = open("compr.txt", "w")
#string = ''.join([chr(int(b, 2)) for b in bit_string])
#print(len(string))
#f.write(string)


fb = open("compr.bin", "wb")
fb.write(bytearray([int(b, 2) for b in bit_string]))

# decoding back into png
# decode
# with open("key.txt", 'r') as f:
#     line = f.readlines()
#     height, width = line[0].split('X')

# class Tri_Node:

# 	def __init__(self, left=None, right=None):
# 		self.left = left
# 		self.right = right




# new_image = Image.fromarray(array)
# new_image.save('new.png')
