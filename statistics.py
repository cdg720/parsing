from bllipparser import Tree
from numpy import mean
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
	return [xx / len(trees) for x in dist]

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
		f = gzip.open(sys.argv[1], 'rb')
	else:
		f = open(sys.argv[1], 'r')
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
	a = "(S1 (SINV (S-TPC-1 (`` ``) (NP-SBJ (EX There)) (VP (VBZ 's) (NP-PRD (NP (DT a) (NN possibility)) (PP (IN of) (NP (NP (DT a) (NN surprise)) ('' '') (PP-LOC (IN in) (NP (DT the) (NN trade) (NN report)))))))) (, ,) (VP (VBD said)) (NP-SBJ (NP (NNP Michael) (NNP Englund)) (, ,) (NP (NP (NN director)) (PP (IN of) (NP (NN research))) (PP (IN at) (NP (NNP MMS))))) (. .)))"
	b = "(S1 (SINV (`` `) (S (`` `) (NP (EX There)) (VP (AUX 's) (NP (NP (DT a) (NN possibility)) (PP (IN of) (NP (NP (DT a) (NN surprise) (POS ')) ('' ') (PP (IN in) (NP (DT the) (NN trade) (NN report)))))))) (, ,) (VP (VBD said)) (NP (NP (NNP Michael) (NNP Englund)) (, ,) (NP (NP (NN director)) (PP (IN of) (NP (NN research))) (PP (IN at) (NP (NNP MMS))))) (. .)))"
	print evaluate(a, b)

	# trees, scores = read_nbest(sys.argv[1])
	# gold = read_gold(sys.argv[2])

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

	
main()

	
