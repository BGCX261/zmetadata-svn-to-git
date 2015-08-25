from threading import Thread
import ping
import time

class MultiPinger(Thread):
    stopped = False
    
    def __init__(self, addresses, timeBetweenPingBatches = 30):
        ''' MultiPinger(list<address:string>, timeBetweenPingBatchesSeconds:int)'''
        Thread.__init__(self)
        self.setDaemon(True)
        self.addresses = {}
        for address in addresses:
            self.addresses[address] = (0,-1,0)
        self.timeBetweenPingBatches = timeBetweenPingBatches
        self.start()        

    def addAddress(self, address):
        self.addresses[address] = (0,-1,0)   
        
    def getAddresses(self):
        return self.addresses.keys() 

    def stop(self):
        self.stopped = True
        
    def run(self):
        while not self.stopped:
            for address in self.addresses:
                average, timeout = ping.pingN(address, 5)
                if self.stopped:
                    break
                self.addresses[address] = (self.addresses[address][0]+1,average, timeout)
            time.sleep(self.timeBetweenPingBatches)
                
    def getStats(self):
        '''Get ping statistics:
                returns : map<address, tuple<pingcount:int, average_ms:float, timeoutcount:int>
        '''
        return self.addresses

if __name__ == "__main__":

    # set up the list of addresses to ping
    addresses = ["10.50.130.52"]
    #addresses = ["www.fdsfdseewes.com","10.50.130.52","10.50.130.53","www.google.co.za"]        
    
    # create the multipinger, ginving the list and 1second between ping batches
    # this creates AND starts the multiplinger thread
    # note, addresses CANNOT be added - stop the pinger, destroy it and create a new one
    mp = MultiPinger(addresses,5)
    for i in range(10):
        time.sleep(10)        
        # get the stats object from the pinger
        # stats is a map<address:string, tuple<totalbatchcount:int, lastaveragems:float, lasttimeouts:int>
        stats = mp.getStats()
        print "\n"
        for key in addresses:
            print key + " pinged "+str(stats[key][0])+" times, average "+ str(stats[key][1]) + "ms, ("+str(stats[key][2])+" timeouts) for last ping"
        print "-"*40
    
    # stop the pinger - it may take a while to stop
    mp.stop()
    