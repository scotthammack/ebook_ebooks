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
END_PUNCT = re.compile('[!?.]"?$')

client = pytumblr.TumblrRestClient(
	TUMBLR_AUTH[0], TUMBLR_AUTH[1], TUMBLR_AUTH[2], TUMBLR_AUTH[3]
)

output = ''

def assemble_corpus(database):
	source_file = open(database,'r')
	source = source_file.readlines()
	source_file.close()

	corpus = []

	for line in source:
		for word in line.split():
			corpus.append(word)
	return corpus

titles = ('Mr.', 'Mrs.', 'Dr.', 'Ms.')

def start_of_sentence(pos):
	return corpus[pos].istitle() and not corpus[pos - 1].endswith(titles) and re.search(END_PUNCT, corpus[pos - 1])

def end_of_sentence(pos):
	return corpus[pos + 1].istitle() and not corpus[pos].endswith(titles) and re.search(END_PUNCT, corpus[pos])
	#return re.search(END_PUNCT, corpus[pos]) and corpus[pos + 1].istitle() and not corpus[pos].endswith(titles)


def get_start_pos():
	while True:
		pos = random.randint(0, len(corpus) - 1)
		if start_of_sentence(pos):
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

def finish_para(text):
	text = text.strip()
	last_quote_pos = text.rfind('"')
	first_quote_pos = text.find('"')
	if last_quote_pos == 0 or text[last_quote_pos - 1] is ' ':
		text += '"'
	elif first_quote_pos == len(text) -1 or text[first_quote_pos + 1] is ' ':
		text = '"' + text
	open_parens = count_char(text, '(')
	closed_parens = count_char(text, ')')
	for i in range(0, (open_parens - closed_parens)):
		text += ')'
	text += '\n\n'
	return text

def create_sentence(pos):
	sentence = ''

	while not end_of_sentence(pos) and len(output) <= OUTPUT_LENGTH - len(corpus[pos]):
		sentence += corpus[pos] + ' '
		if random.random() <= JUMP_PROB:
			word_to_look_for = corpus[pos + 1]
			pos = get_word_pos(word_to_look_for)
		else:
			pos += 1
	
	return sentence + corpus[pos]

def create_para(pos):
	para = ''

	while not random.random() <= PARAGRAPH_BREAK_PROB and len(output) < OUTPUT_LENGTH - len(para) or len(para) < 1:
		para += create_sentence(pos) + ' '
		pos = get_start_pos()
	
	para = finish_para(para)

	return para


def create_post(corpus):
	output = ''

	while len(output) <= OUTPUT_LENGTH:

		pos = get_start_pos()
		new_para = create_para(pos)

		if len(output) + len(new_para) <= OUTPUT_LENGTH:
			output += new_para
		else:
			break

#		if not position or position >= len(corpus):
#			sentence = finish_sentence(sentence + word_to_look_for, True)
#			sentence = finish_para(sentence)
			#sentence += word_to_look_for + '. '
#			break
#		else:
#			if not new_paragraph:
#				sentence += ' '
	
	return output.strip()


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

#client.create_text(TUMBLR_NAME, state="published", title=post_title(),
#	body=output)
