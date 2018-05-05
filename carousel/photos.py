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
import log

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
    photoDirs = glob.glob( '{}/*.[0-9][0-9]'.format(photoRoot) )
    log.debug(photoDirs)
    log.debug('photoDirs: {}'.format(photoDirs) )
    for i in photoDirs:
        number = float(i[-2:])/100
        log.debug( 'found a level {} '.format(number))
        fileLevels[number].extend ( getPhotos(i)  )

    for level in fileLevels.keys():
        for filename in fileLevels[level]:
            log.debug('{} : {}'.format(level, filename) )
    
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