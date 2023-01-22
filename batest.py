import numpy as np
from PIL import Image
import heapq
from bitstring import BitArray

# read an image
image_url = "Fotor_AI (1).png"
image = Image.open(image_url)
array = np.array(image)

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

# for key in frequency_table:
#     l.append(Node(frequency_table[key], str(key)))



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
width, height, deapth = array.shape

# put decode and dimensions into a ... file 

f = open("compr.bin", "wb")
huffman_img = ''
for row in range(array.shape[0]):
    for col in range(array.shape[1]):
        huffman_img += decode[tuple(array[row][col])]

bits = BitArray(bin=huffman_img)
bits.tofile(f)
# f.write(bits)

# decoding back into png
new_image = Image.fromarray(array)
new_image.save('new.png')bl