import sys
import os
sys.path.append("../..")
from util import reglob

ROOT = '/tmp/'
dirs = [os.path.join(ROOT, d) for d in ["simplename", "onedigit.1", "twodigts.12", "threeletters.abc"] ]

for i in dirs:
    print(i)
    os.mkdir( i )
print('test')

a = reglob.reglob(ROOT,'.*\.[0-9]+' )

a = list(a)
print(a)

for i in dirs:
    os.rmdir(i)

