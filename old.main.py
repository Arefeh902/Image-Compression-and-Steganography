import numpy as np
from PIL import Image
import heapq
import pickle

# read an image
image_url = "Fotor_AI.png"
image = Image.open(image_url)
array = np.array(image)

# initializing frequency table
frequency_table = {}
# for row in array:
#     for element in row:
#         frequency_table[tuple(element)] = 0

# for row in array:
#     for element in row:
#         frequency_table[tuple(element)] += 1


unique, count = np.unique(array, return_counts=True)
for i in range(unique.shape[0]):
	frequency_table[unique[i]] = count[i]

print(frequency_table)
print(unique, count)

# huffman coding
class Node():
    freq: int
    symbol: tuple

    def __init__(self, freq, symbol: int = None, left = None, right = None) -> None:
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

    heapq.heappush(heap, Node(left.freq+right.freq, '', left, right))

root = heap[0]
decode = {}

def traverse(n: Node, s: str):
    if n.left is None:
        decode[n.symbol] = s
        return
    traverse(n.left, s+'0')
    traverse(n.right, s+'1')

traverse(root, '')
height, width, deapth = array.shape
print(array.shape)

print(decode)

with open("key.pickle", 'wb') as f:
    decode['height'] = height
    decode['width'] = width
    pickle.dump(decode,f)


binary_string = ''
for row in range(array.shape[0]):
    for col in range(array.shape[1]):
    	for dep in range(array.shape[2]):
	        binary_string += decode[array[row][col][dep]]

# print(binary_string)

f = open("compr.txt", "w")
bit_string = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

string = ''.join([chr(int(b, 2)) for b in bit_string])
print(string)
f.write(string)


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
