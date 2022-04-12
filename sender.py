from shared import *

class sender:
    RTT = 20
    setter = 0
    
    def isCorrupted (self, packet):
        result1 = False    #not corrupted
        computed_checksum = checksumCalc(packet.payload)    #payload checksum 
        if computed_checksum != packet.checksum:   #if received checksum is not the same as packet checksum
            result1 = True

        return result1

    def isDuplicate(self, packet):
        result2 = False    #not duplicate
        if packet.ackNum != self.seqNum:    #if the acknowledgement number is not the same as sequence number
            result2 = True    #duplicate
        return result2
 
    def getNextSeqNum(self):
        if self.seqNum == 0:
            self.seqNum = 1
        else:
            self.seqNum = 0
        return

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        self.seqNum = 0
        self.ackNum = 0
        self.packet = None
        return

    def timerInterrupt(self):
        #self.networkSimulator.stopTimer(self.entity)                   #stop timer
        self.networkSimulator.udtSend(self.entity, self.packet)        #resend packet
        self.networkSimulator.startTimer(self.entity, 2*sender.RTT)    #restart timer
        
        return


    def output(self, message):
        if sender.setter == 0:
            sender.setter = 1
            self.checksum = checksumCalc(message.data)     #payload checksum 
            self.packet = Packet(self.seqNum, self.ackNum, self.checksum, message.data)      #create packet object
            self.networkSimulator.udtSend(self.entity, self.packet)        #send packet
            self.networkSimulator.startTimer(self.entity, sender.RTT)      #start timer

        return
 
    
    def input(self, packet):
        result1 = self.isCorrupted(packet)
        result2 = self.isDuplicate(packet)

        if result1 == False and result2 == False:      #if not corrupted and not duplicated
            self.packet = None               #set packet to None
            self.getNextSeqNum()             #get the next sequence number
            self.networkSimulator.stopTimer(self.entity)     #stop timer
            sender.setter = 0

        return
