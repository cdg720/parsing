import gzip
import string
import sys

# NYT only. check for other coropra.
def clean_sentences():
	if len(sys.argv) == 1:
		print 'usage: python clean_sentences.py file1 file2 ... out'
		print 'e.g.: python clean_sentences.py ~/data/gigaword/nyt/*.gz /pro/dpg/dc65/data/gigaword/chunks/nyt'
		sys.exit(0)

	doc_size = 500
	out = sys.argv[-1]
	i = 0
	g = None

	x = [0,] * 2
	for doc in sys.argv[1:-1]:
		f = gzip.open(doc, 'rb')
		y = [0,] * 2
		for line in f.read().splitlines():
			count = 0
			count2 = 0
			if line[22:24] == '> ':
				processed = line[24:-6]
			elif line[23:25] == '> ':
				processed = line[25:-6]				
			elif line[24:26] == '> ':
				processed = line[26:-6]				
			else:
				print line
			for ch in processed:
				if ch.islower():
					count += 1
				if ch != ' ':
					count2 += 1
			x[1] += 1
			y[1] += 1
			if count * 100 / count2 >= 90: # go back to 90
				x[0] += 1
				y[0] += 1
				if i % doc_size == 0: # new file
					if g:
						g.flush()
						g.close()
					g = gzip.open(out + '/' + str(i / doc_size + 1) + '.gz', 'wb')
				g.write(line + '\n')
				i += 1
		print doc, y, x

def clean_sentences2():
	if len(sys.argv) == 1:
		print 'usage: python clean_sentences.py file1 file2 ... out'
		print 'e.g.: python clean_sentences.py ~/data/gigaword/nyt/*.gz /pro/dpg/dc65/data/gigaword/chunks/nyt'
		sys.exit(0)

	doc_size = 500
	out = sys.argv[-1]
	i = 0
	g = None

	x = [0,] * 2
	for doc in sys.argv[1:-1]:
		f = gzip.open(doc, 'rb')
		y = [0,] * 2
		for line in f.read().splitlines():
			x[1] += 1
			y[1] += 1
			x[0] += 1
			y[0] += 1
			if i % doc_size == 0: # new file
				if g:
					g.flush()
					g.close()
				g = gzip.open(out + '/' + str(i / doc_size + 1) + '.gz', 'wb')
			g.write(line + '\n')
			i += 1
		print doc, y, x

clean_sentences2()
