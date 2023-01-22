import numpy as np
from PIL import Image
import pickle

class TriNode:
	
	def __init__(self, symbol:tuple=(), left=None, right=None):
		self.symbol = symbol
		self.left = left
		self.right = right


def create_tri_element(n: TriNode, s: str, t: tuple):
	if s == '':
		n.symbol = t
		return
	e = s[0]
	if e == '0':
		if n.left == None:
			n.left = TriNode()
		create_tri_element(n.left, s[1:], t)
	elif e == '1':
		if n.right == None:
			n.right = TriNode()
		create_tri_element(n.right, s[1:], t)
	

def print_tri(n):
	if n.left != None:
		print_tri(n.left)
	if n.right != None: 
		print_tri(n.right)
	print(n.symbol)


# decode = {}
# with open("key.txt", 'r') as f:
# 	lines = f.readlines()
# 	height, width = lines[0].split('X')
# 	for line in lines[1:]:
# 		key, value = line.split(':')
# 		print((key))
# 		decode[tuple(key)] = value


f = open('key.pickle', 'rb')
decode = pickle.load(f)
root = TriNode()
for key in decode:
	if key in ['height', 'width']:
		continue
	s = decode[key]
	create_tri_element(root, s, key)

height, width = decode['height'], decode['width']

decoded_data = []
f = open('compr.bin', 'rb') 
data = f.read()
print(len(data))
# data = data.decode()
data = ''.join([bin(s)[2:].zfill(8) for s in data])

# f = open('compr.txt', 'r')
# data = f.read()
# data = ''.join([bin(ord(s))[2:].zfill(8) for s in data])
print(data[:200]) 
print(len(data))

def decode_(data):
	n = root
	i = 0
	while i < len(data):
		print(i)
		if data[i] == '0':
			if n.left != None:
				n = n.left
			else: 
				decoded_data.append(n.symbol)
				n = root
				i -= 1

		elif data[i] == '1':
			if n.right != None:
				n = n.right
			else: 
				decoded_data.append(n.symbol)
				n = root
				i -= 1
		i += 1
	return decoded_data

decoded_data = decode_(data)
decoded_data.append(n.symbol)
print(len(decoded_data))

array = np.array(decoded_data)
print(array.shape)
array = np.reshape(array, (height, width, 4))

new_image = Image.fromarray(array)
new_image.save('new.png')