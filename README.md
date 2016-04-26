# ebook\_ebooks
ebook\_ebooks is a simple text generator for shuffling text into English-like
but meaningless sentences and paragraphs. It's pretty bare-bones, but does
include a few features to improve readability, such as chapter numbering,
paragraph breaks, and parenthesis/quotation mark balancing.

An example of ebook\_ebooks in action can be found at
[ebook-ebooks.tumblr.com](https://ebook-ebooks.tumblr.com/).

## Dependencies
This version is configured to post to Tumblr and thus depends on pytumblr.

## Configuration
For posting to Tumblr, ebook\_ebooks looks for a file called
tumblr\_secrets.py, which should contain your Tumblr keys and blog
name, as well as the filename you want to use for the corpus. A sample
tumblr\_secrets.py:

	#!/usr/local/bin/python
	# coding: utf-8
	
	TUMBLR_AUTH = [ 'consumer key goes here',
	  'consumer secret goes here',
	  'access key goes here',
	  'access secret goes here'
	]
	
	TUMBLR_NAME = 'ebook-ebooks'
	DATABASE = 'corpus.txt'

## Customization
The following constants may be adjusted to fine-tune the output.

OUTPUT\_LENGTH (default: 1400) is the maximum length of the output, in
characters. The generator will keep running until the output hits this length,
at which point it cut off the output at the end of the last completed
sentence.

PARAGRAPH\_BREAK\_PROB (default: 0.25) is the probability of starting a new
paragraph when the end of a sentence is reached.

JUMP\_PROB (default: 0.2) is the probability of jumping to a different
position in the corpus on each word. If this succeeds, it scans the corpus
for other instances of the same word, then picks one of those instances at
random to jump to. (If no other instances are found, it will simply pick
the same instance and continue with no jump.)

END\_PUNCT is a regular expression that defines the punctuation that the
script should consider to mark the end of a sentence. It defaults to an
exclamation mark, question mark, or period, optionally followed by a
quotation mark.

## Contact
The author of ebook\_ebooks is me, Scott Hammack. I can be reached by
email at <shammack@protonmail.com> or on Twitter as
@[czircon](https://twitter.com/czircon/).
