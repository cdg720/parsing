import sys
import numpy as np

if len(sys.argv) < 2:
	print 'usage: python analyze.py sent-sel/*'
	sys.exit(0)

tmp = []
for x in sys.argv[1:]:
	f = open(x + '/result.txt')
	lines = f.read().splitlines()
	score = float(lines[-14].split()[3])
	num = int(x.split('/')[-1])
	tmp.append([score, num])

tmp = np.array(tmp)
tmp = tmp[tmp[:,0].argsort()]
scores = np.array([x[0] for x in tmp])
print len(scores)
print scores
print np.mean(scores)
print np.median(scores)
print np.max(scores)
print np.min(scores)
print tmp[-25:]
print np.mean(scores[-25])

