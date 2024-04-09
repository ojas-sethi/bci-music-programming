import TGCHandler
import time


handler = TGCHandler.TGCHandler(host = '192.168.137.224')
handler.connect()
handler.configure()
handler.startMeasuring()
while True:
    att = handler.get('attention')
    plevel = handler.get('poorSignalLevel')
    med = handler.get('meditation')
    if att != None and plevel != None:
        print("Att:" + str(att) + " Sig:" + str(plevel) + " Med:" + str(med))
        if att > 70:
            print("Super Conc!")
        if med > 60 and att < 70:
            print("DATAAAAAAA")
        
    else:
        print(":(")
    time.sleep(1)