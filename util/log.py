import sys

# Import logging so we can see the log level numbers
import logging
# Also import it into current namespace so calling modules have direct access
from logging import *

from . import config


# set up logging to file - see previous section for more details
LONGFORMAT='%(levelname)8s: ''%(asctime)s''%(filename)-20s: ''%(lineno)4d:\t''%(message)s'
SHORTFORMAT='%(levelname)-8s: %(message)s'

# Root logger gets everything.  Handlers defined below will filter it out...

getLogger('').setLevel(DEBUG)

def init( filename ):
    filehandler = FileHandler(filename,mode='w')
    filehandler.setLevel(INFO)
    filehandler.setFormatter(Formatter(LONGFORMAT))
    getLogger('').addHandler(filehandler) 
    info('logging initialized')



# define a Handler which writes to sys.stderr
console = StreamHandler()
logLevelNumber = getattr( logging, config.logLevel )
console.setLevel( logLevelNumber )
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger('').addHandler(console)
