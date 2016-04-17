#!/usr/local/bin/python
# coding: utf-8

import random

source_file = open("gatsby.txt","r")
source = source_file.readlines()
source_file.close()

corpus = []


def get_start_pos():
	acceptable = False
	while not acceptable:
		pos = random.randint(0, len(corpus)-1)
		if corpus[pos].istitle():
			acceptable = True
	return pos

def get_word_pos(target):
	counter = 0
	instances = []
	for word in corpus:
		if word == target:
			instances.append(counter)
		counter += 1
	if instances:
		return random.choice(instances)
	else:
		return None

for line in source:
	for word in line.split():
		corpus.append(word)

# print len(corpus)
# print position

fullString = ''

for i in range(1,10):
	newString = ''
	position = get_start_pos()

	while len(newString) < 1400 - len(corpus[position]):
		newString += corpus[position]

		if random.randint(1, 5) == 1:
			word_to_look_for = corpus[position+1]
			position = get_word_pos(word_to_look_for)
		else:
			position += 1
		if not position or position >= len(corpus):
			newString += word_to_look_for + '. '
			break
		else:
			newString += ' '

	fullString += newString	+ "\n"

print fullString
