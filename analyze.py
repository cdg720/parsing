import sys
import numpy as np

def write():
	if len(sys.argv) < 2:
		print 'usage: python analyze.py sent-sel/*'
		sys.exit(0)
	
	tmp = []
	for x in sys.argv[1:]:
		f = open(x + '/result.txt')
		lines = f.read().splitlines()
		score = float(lines[-14].split()[3])
		prec = float(lines[-15].split()[3])		
		rec = float(lines[-16].split()[3])
		num = int(x.split('/')[-1])
		tmp.append([num, rec, prec, score])

	tmp = np.array(tmp)
	tmp = tmp[tmp[:,0].argsort()]
	print 'id\trec\tprec\tscore'
	for t in tmp:
		print '%d\t%.2f\t%.2f\t%.2f' % (t[0], t[1], t[2], t[3])

#write()

def read():
	if len(sys.argv) != 2:
		print 'usage: python analyze.py result/sent-sel/#'
		sys.exit(0)

	f = open(sys.argv[1], 'r')
	tmp = []
	for line in f.read().splitlines()[1:]:
		tokens = line.split()
		tmp.append([float(tokens[3]), int(tokens[0])])
	tmp = np.array(tmp)
	tmp = tmp[tmp[:,0].argsort()]
	scores = np.array([x[0] for x in tmp])
	print len(scores)
	print ','.join([str(x) for x in scores])
	#print scores
	print 'mean:', np.mean(scores)
	print 'median:', np.median(scores)
	print 'max:', np.max(scores)
	print 'min:', np.min(scores)
	top = 25
	print ' '.join([str(int(x[1])) for x in tmp[-top:]])
	print 'top %d mean:' % top, np.mean(scores[-top])

read()

