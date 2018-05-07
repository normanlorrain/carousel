import subprocess
import time

import itertools 
import collections
import glob
import signal
import os
# import pyinotify  #Does not work over SMB or shared folders. Need to poll; crap.
import sys


from . import log

class Supervisor():
    def __init__( self, watchDir, listfile, updateListFn ):
        self.watchDir = watchDir
        self.dirTime = os.path.getmtime(self.watchDir)
        self.listfile = listfile
        self.updateListFn = updateListFn
        self.itemList = self.updateListFn( self.watchDir )
        self.writeList( self.itemList )
        self.processList = []
        signal.signal( signal.SIGTERM, self.term )

    def term(self, sig, frame):
        log.info("sigterm")
        self.stopProcesses()
        sys.exit(0)

    def startProcess(self, arglist):
        proc = subprocess.Popen( arglist )
        log.info('started {}'.format(proc) )
        self.processList.append( proc )

    def stopProcesses(self):
        for i in self.processList:
            log.info('stopping {}'.format(i) )
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

    def detectChanges(self):
        mtimes = []
        for root, _, _ in os.walk(self.watchDir):
            mtimes.append(os.path.getmtime(root))

        # Get the latest mod time
        newTime = max(mtimes)

        if self.dirTime != newTime:
            self.dirTime = newTime
            return True
        else:
            return False

    def monitor(self):
        while True:
            try:
                time.sleep(10) 
                if self.detectChanges():
                    log.info('detected changes')
                    self.itemList = self.updateListFn(self.watchDir)
                    self.writeList( self.itemList )
                    self.restartProcesses()
                else:
                    log.debug('no change')
                    


            except KeyboardInterrupt:
                self.term(None, None)



def main():
    print("test")

if __name__ == '__main__':
    main()