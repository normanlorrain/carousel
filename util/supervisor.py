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
        self.inputWatchDir = watchDir
        self.outputListFile = listfile
        self.updateListFn = updateListFn
        self.dirTime = os.path.getmtime(self.inputWatchDir)
        
        self.updateOutputList()
        self.processList = []
        self.argsList = []
        signal.signal( signal.SIGTERM, self.term )

    def term(self, sig, frame):
        log.info("sigterm")
        self.stopProcesses()
        sys.exit(0)

    def startProcess(self, args ):
        self.argsList.append( args )
        proc = subprocess.Popen( args  )
        log.info(f'started PID:{proc.pid} ARGS: {args}')
        self.processList.append( proc )

    def stopProcesses(self):
        for proc in self.processList:
            log.info(f'stopping PID:{proc.pid} ARGS: {proc.args}')
            proc.terminate()
            proc.wait()

    def restartProcesses(self):
        savedArgsList = self.argsList
        self.argsList = []
        self.processList = []
        for i in savedArgsList:
            self.startProcess(i)

    def updateOutputList(self):
        log.debug('updateOutputList')
        itemList =  self.updateListFn(self.inputWatchDir)
        with open(self.outputListFile, 'w') as f:
            if itemList:
                for line in itemList:
                    f.write( line ) 
                    f.write('\n')
            else:
                log.error("nothing to put into output list file")

    def detectChanges(self):
        mtimes = []
        for root, _, _ in os.walk(self.inputWatchDir):
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
                    self.stopProcesses()
                    self.updateOutputList()
                    self.restartProcesses()
                else:
                    log.debug('no change')
                    


            except KeyboardInterrupt:
                self.term(None, None)



def main():
    print("test")

if __name__ == '__main__':
    main()