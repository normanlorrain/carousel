import log
import supervisor


if __name__ == '__main__':
    import photos
    supervisor = supervisor.Supervisor( "../photos", "~testlist.txt", photos.buildPhotoList )
    process = ['/usr/bin/xclock']
    supervisor.startProcess( process )
    supervisor.monitor()
    
 
