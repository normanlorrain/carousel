import subprocess
import time
import logging as log

import itertools 
import collections
import glob
import signal
import os
# import pyinotify  #Does not work over SMB or shared folders. Need to poll; crap.
import sys




class Supervisor():
    def __init__( self, listfile, updateListFn ):
        self.listfile = listfile
        self.updateListFn = updateListFn
        self.itemList = self.updateListFn()
        self.writeList( self.itemList )
        self.processList = []
        signal.signal( signal.SIGTERM, self.term )

    def term(self, sig, frame):
        print("sigterm")
        self.stopProcesses()
        sys.exit(0)

    def startProcess(self, arglist):
        proc = subprocess.Popen( arglist )
        print('started', proc)
        self.processList.append( proc )

    def stopProcesses(self):
        for i in self.processList:
            print('stopping', i)
            i.terminate()
            i.wait()

    def restartProcesses(self):
        oldList = self.processList
        self.stopProcesses()
        self.processList = []
        for i in oldList:
            self.startProcess(i.args)



    def writeList(self, itemlist ):
        with open(self.listfile, 'w') as f:
            for line in itemlist:
                f.write( line ) 
                f.write('\n')



    def monitor(self):
        while True:
            try:
                time.sleep(10) 
                newList = self.updateListFn()

                if self.itemList != newList:
                    self.itemList = newList
                    print('detected changes')
                    self.writeList( self.itemList )
                    self.restartProcesses()
                else:
                    print('no change')
                    


            except KeyboardInterrupt:
                self.term(None, None)

        
