import subprocess
import time

import itertools 
import collections
import glob
import signal
import os
import random
# import pyinotify  #Does not work over SMB or shared folders. Need to poll; crap.
import sys


from . import log
from . import reglob

def getPhotos( path ):
    log.debug( 'getphotos {}'.format( path ) )
    all = glob.glob('{}/*.jpg'.format( path) )
    all.extend( glob.glob('{}/*.jpeg'.format( path) ) )
    all.extend( glob.glob('{}/*.png'.format( path) ) )
    return all

def buildPhotoList(photoRoot):
    log.debug('buildphotolist')
    fileList = []

    fileLevels = collections.defaultdict(list)
    photoDirs = reglob.reglob( photoRoot, r'.*\.[0-9]+' )
    log.debug(photoDirs)
    log.debug('photoDirs: {}'.format(photoDirs) )
    for i in photoDirs:
        dirname,ext = os.path.splitext(i)
        weight = float(ext)
        log.debug( f'Directory {dirname}, weight {weight} ')
        fileLevels[weight].extend ( getPhotos(i)  )

    if len(fileLevels) == 0:
        return None
    # for level in fileLevels.keys():
    #     for filename in fileLevels[level]:
    #         log.debug('{} : {}'.format(level, filename) )
    
    weightedIterators = {}
    for level in fileLevels.keys():
        weightedIterators[level] = itertools.cycle(fileLevels[level])



    for i in range(1000):
        weights = list(weightedIterators.keys())
        photoIterators = list(weightedIterators.values())
        # print('values', values)
        #print('keys', keys)
        randomIterator = random.choices( photoIterators, weights)[0]
        #print('randomIterator',randomIterator)
        filename = next(randomIterator)
        #log.debug( filename ) 
        fileList.append( filename )

    log.debug('LIST COMPLETE')
    for f in fileList:
        log.debug('   {}'.format(f))

    return fileList
