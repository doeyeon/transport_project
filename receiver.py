from shared import *

class receiver:
    
    def isCorrupted(self, packet):
        result1 = False       #packet not corrupted
        computed_checksum = checksumCalc(packet.payload)   #payload checksum 
        if computed_checksum != packet.checksum:      #if the computed checksum is not the same as the packet checksum
            result1 = True    #packet corrupted

        return result1
   
    def isDuplicate(self, packet):
        result2 = False      #packet is not duplicate
        if self.seqNum != packet.seqNum:     #if expected seqNum is not packet seqNum
            result2 = True    #packet is duplicate
        return result2
    
    def getNextExpectedSeqNum(self):
        temp = 0
        if self.seqNum == 0:
            temp = 1
        else:
            temp = 0
        return temp
    
    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self):
        self.seqNum = 0
        self.ackNum = 0
        return
         

    def input(self, packet):
        result1 = self.isCorrupted(packet)
        result2 = self.isDuplicate(packet)

        if result1 == False and result2 == False:     #if not corrupted and not duplicate
            self.networkSimulator.deliverData(self.entity, packet)
            self.checksum = packet.checksum
            self.packet = Packet(packet.seqNum, self.ackNum, self.checksum, packet.payload)
            self.networkSimulator.udtSend(self.entity, self.packet)
            self.seqNum = self.getNextExpectedSeqNum()
            self.ackNum = self.seqNum
        else:                               #if either corrupted or duplicate or both
            self.ackNum = self.getNextExpectedSeqNum()
            self.packet = Packet(packet.seqNum, self.ackNum, packet.checksum, packet.payload)
            self.networkSimulator.udtSend(self.entity, self.packet)

        return
