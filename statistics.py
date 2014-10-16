from bllipparser import Tree
from numpy import mean, median
from subprocess import Popen, PIPE, call
import gzip
import sys

def compute_dist(gold, trees):
	dist = [0.,] * 50
	for g, t in zip(gold, trees):
		argmax = 0
		score = evaluate(g, t[0])
		for i in xrange(1, len(t)):
			x = evaluate(g, t[i])
			if x > score:
				argmax = i
				score = x
		dist[argmax] += 1
	return [x / len(trees) for x in dist]

def create_separate_files(trees, gold):
	ind = 0
	# for ts, g in zip(trees, gold):
	# 	ind += 1
	# 	f = gzip.open('/home/dc65/Documents/research/self-training/code/tmp/dev/' + str(ind) + '/pred.gz', 'wb')
	# 	h = gzip.open('/home/dc65/Documents/research/self-training/code/tmp/dev/' + str(ind) + '/gold.gz', 'wb')
	# 	for t in ts:
	# 		f.write(str(t) + '\n')
	# 		h.write(str(g) + '\n')
	# 	f.close()
	# 	h.close()

def evaluate(sent1, sent2): # sent1: gold?
	score = 0
	f = open('/home/dc65/Documents/research/self-training/code/tmp/a', 'w')
	f.write(str(sent1) + '\n')
	f.flush()
	f.close()
	f = open('/home/dc65/Documents/research/self-training/code/tmp/b', 'w')
	f.write(str(sent2) + '\n')					
	f.flush()
	f.close()
	out, err = None, None
	p = Popen(['/home/dc65/Documents/tools/bllip_parser/bllip-parser-master/SParseval/src/sparseval', '-v', '-h', '/home/dc65/Documents/tools/bllip_parser/bllip-parser-master/SParseval/headInfo.txt', '-p', '/home/dc65/Documents/tools/bllip_parser/bllip-parser-master/SParseval/SPEECHPAR.prm', '/home/dc65/Documents/research/self-training/code/tmp/a', '/home/dc65/Documents/research/self-training/code/tmp/b'], stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()
	call(['rm', '/home/dc65/Documents/research/self-training/code/tmp/a'])
	call(['rm', '/home/dc65/Documents/research/self-training/code/tmp/b'])
	try:
		return float(out.split('\n')[13].split()[-1])
	except:
		print sent1
		print sent2
		print out
		sys.exit(0)

def read_gold(path):
	if path.endswith('.gz'):
		f = gzip.open(sys.argv[2], 'rb')		
	else:
		f = open(sys.argv[2])
	gold = [Tree(x) for x in f.read().splitlines()]
	return gold	

def read_nbest(path):
	if path.endswith('.gz'):
		f = gzip.open(path, 'rb')
	else:
		f = open(path, 'r')
	tmp = f.read().splitlines()
	x = tmp[::2]
	y = tmp[1::2]

	trees, scores, tmp1, tmp2 = [], [], [], []
	prev = 1
	for tree, score in zip(x, y):
		score = float(score)
		if score > prev: # new
			if tmp1:
				trees.append(tmp1)
				scores.append(tmp2)
				tmp1, tmp2 = [Tree(tree)], [score]
			prev = score
		else:
			prev = score
			tmp1.append(Tree(tree))
			tmp2.append(score)
	if tmp1:
		trees.append(tmp1)
		scores.append(tmp2)
	return trees, scores

def main():
	if len(sys.argv) != 3:
		print 'usage: python statistics.py 50best gold'
		sys.exit(0)

	trees, scores = read_nbest(sys.argv[1])
	gold = read_gold(sys.argv[2])

	# create_separate_files(trees, gold)
	# best_scores = []
	# bins = [0,] * 10	
	# for score in scores:
	# 	best_scores.append(score[0])
	# 	bins[int(score[0] * 10)] += 1

	#print best_scores
	# print mean(best_scores)
	# print sum(best_scores)
	# print median(best_scores)
	# print max(best_scores)
	# print min(best_scores)
	# x = [float(x) / len(best_scores) for x in bins]
	# print '\t'.join([str(xx * 10) + '-' + str((xx+1) * 10) for xx in xrange(10)])
	# print '\t'.join(['%.4f' for xx in xrange(10)]) % (tuple(x))
	# empirical_dist = compute_dist(gold, trees)
	# print 'empirical distribution:'
	# print empirical_dist

	# x = [[] for x in xrange(50)]
	# for ss in scores:
	# 	for i in xrange(len(ss)):
	# 		x[i].append(ss[i])			
	# predicted_dist = [mean(xx) for xx in x]
	# print 'rerakning parser distribution:'
	# print predicted_dist
	
#main()

	
