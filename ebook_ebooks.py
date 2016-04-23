#!/usr/local/bin/python
# coding: utf-8

import json
import pytumblr
import random
import re

from tumblr_secrets import TUMBLR_AUTH, DATABASE, TUMBLR_NAME

OUTPUT_LENGTH = 1400
PARAGRAPH_BREAK_PROB = 0.25
JUMP_PROB = 0.2

client = pytumblr.TumblrRestClient(
	TUMBLR_AUTH[0], TUMBLR_AUTH[1], TUMBLR_AUTH[2], TUMBLR_AUTH[3]
)


def assemble_corpus(database):
	source_file = open(database,'r')
	source = source_file.readlines()
	source_file.close()

	corpus = []

	for line in source:
		for word in line.split():
			corpus.append(word)
	return corpus


def get_start_pos():
	while True:
		pos = random.randint(0, len(corpus) - 1)
		if corpus[pos].istitle():
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

def count_char(text, target):
	count = 0
	for character in text:
		if character is target:
			count += 1
	return count

def finish_sentence(text, add_period):
	open_parens = count_char(text, '(')
	closed_parens = count_char(text, ')')
	for i in range(0, (open_parens - closed_parens)):
		text += ')'
	if add_period:
		text += '.'
#	text += ' '
	return text

def finish_para(initial_text):
	currently_unclosed = False
	last_quote_pos = 0
	text = list(initial_text)
	for i in range(0, len(initial_text)):
		if text[i] is '"':
			if not text[i-1] or text[i-1] is ' ' or text[i-1] is '\n':	# opening quote
				if currently_unclosed:
					# insert a quote somewhere before here to turn this into a closing quote
					current_unclosed = False
				else:
					currently_unclosed = True
		#	elif i >= len(text) or not text[i+1] or text[i+1] is ' ' or text[i+1] is '\n':	# closing quote
		#		if currently_unclosed:
	#				currently_unclosed = False
					# remove this char?
			last_quote_pos = i
	if currently_unclosed:
		text = "".join(text) + '"'
	return "".join(text) + '\n\n'

def create_post(corpus):
	output = ''
	sentence = ''

	position = get_start_pos()

	while len(output) < OUTPUT_LENGTH - len(sentence):

		new_paragraph = False
		sentence += corpus[position]

		if (corpus[position].endswith(('.','?','!','.\"','!\"','?\"'))
				and corpus[position + 1].istitle()
				and not corpus[position].endswith(('Mr.','Mrs.','Dr.','Ms.'))):
			output += finish_sentence(sentence, False)
			if random.random() <= PARAGRAPH_BREAK_PROB:
				output = finish_para(output)
				new_paragraph = True
			sentence = ''

		if random.random() <= JUMP_PROB:
			word_to_look_for = corpus[position + 1]
			position = get_word_pos(word_to_look_for)
		else:
			position += 1

		if not position or position >= len(corpus):
			sentence = finish_sentence(sentence + word_to_look_for, True)
			sentence = finish_para(sentence)
			#sentence += word_to_look_for + '. '
			break
		else:
			if not new_paragraph:
				sentence += ' '
	
	return output


def post_title():
	most_recent_post = client.posts(TUMBLR_NAME, limit=1)
	most_recent_title = most_recent_post['posts'][0]['title']
	chapter = int(re.search(r'[0-9]*$', most_recent_title).group(0))
	if chapter:
		chapter = str(chapter + 1)
		return "Chapter " + chapter


corpus = assemble_corpus(DATABASE)

output = create_post(corpus)
print output

client.create_text(TUMBLR_NAME, state="published", title=post_title(),
	body=output)
