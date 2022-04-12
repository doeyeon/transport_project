#from Random import *
import random 
from shared import *
from sender import *
from receiver import *
import copy
import sys

class NetworkSimulator:
    def __init__(self):
        print("Initializing Network Simulator")

    
    def initSimulator(self, maxMsgs, loss, corrupt, delay, seed, trace):
        self.maxMessages = maxMsgs
    
        self.lossProb = loss
        self.corruptProb = corrupt
    
        self.avgMessageDelay = delay
    
        self.rand = random.seed(seed)
    
        self.nMsgSim = 0;                   
        self.time = 0.0;                        

        self.trace = trace
    
        self.eventList =  EventList()          
    
        self.sender = sender(A, self)           
    
        self.receiver = receiver(B, self)       



    def runSimulator(self):
        self.sender.init()
        self.receiver.init()

        sum = float(0.0);             
        for i in range(0,1000):
            sum=sum+random.random()
        avg = sum/float(1000.0)
        if avg < 0.25 or avg > 0.75:
            print("It is likely that random number generation on your machine" )
            print("is different from what this emulator expects.  Sorry ")
            sys.exit()
        else:
            print("average = " + str(avg) )

        self.generateNextArrival()

        while True: 
            next_event = self.eventList.removeNext();

            if next_event == None:
                break
                
            if self.trace >= 1:
                print("---------------------------------------")
            if self.trace >= 2:    
                print("")
                print("EVENT time: " + str(next_event.time));

                if (next_event.event_type == EventType.TIMERINTERRUPT):
                    print("Event type:  TIMERINTERRUPT ")
                elif (next_event.event_type == EventType.FROMAPP):
                    print("Event type:  FROMAPP")
                elif (next_event.event_type == EventType.FROMNETWORK):
                    print("Event type:  FROMNETWORK")
                else:
                    print("Event type: " + str(next_event.event_type))


                print("Event entity: " + str(next_event.entity));
            self.time = next_event.time

            if next_event.event_type == EventType.TIMERINTERRUPT:
                if next_event.entity == A:
                    if self.trace >=1 :
                        print("A: sending the last packet again")
                    self.sender.timerInterrupt()
                else:
                    print("INTERNAL PANIC: Timeout for invalid entity")
                    
            elif next_event.event_type == EventType.FROMNETWORK:
                if next_event.entity == A:
                    if self.trace >= 1:
                        print("A: receiving an acknowledgement packet")
                    self.sender.input(next_event.packet)
                elif next_event.entity == B:
                    if self.trace >= 1:
                        print("B: Receiving the data and sending the acknowledgement " + next_event.packet.payload )
                    self.receiver.input(next_event.packet)
                else:
                    print("INTERNAL PANIC: Packet has arrived for unknown entity");
            elif next_event.event_type == EventType.FROMAPP:

                    nextMessage = ''
                    j = chr(((self.nMsgSim - 1) % 26) + 97)
                    for i in range(0, MAXDATASIZE):
                        nextMessage += j
    
                    if self.trace >= 1:
                        print("A: Sending the data " + nextMessage)
                    self.sender.output(Message(nextMessage))
                    
                    if (self.nMsgSim < self.maxMessages):
                        self.generateNextArrival()
                    else:
                        if self.trace >= 1:
                            print("do not schedule: the maximum number of messages is scheduled")    
            else:
                print("INTERNAL PANIC: Unknown event type")


    def generateNextArrival(self):

        x = self.avgMessageDelay * random.random() * 2

        next_event = Event(self.time + x, EventType.FROMAPP, A)
    
        self.eventList.add(next_event);
    
        self.nMsgSim += 1
        
        if self.trace >= 2:
            print("generateNextArrival(): time is " + str(self.time));
            print("generateNextArrival(): future time for " + "event " + str(next_event.event_type) + " at entity " + str(next_event.entity) + " will be " + str(next_event.time));
    

    def startTimer(self, entity, increment):
        if self.trace >= 1:
            print("startTimer: starting timer at " + str(self.time))

        t = self.eventList.removeTimer(entity);

        if (t != None):
            print("startTimer: Warning: Attempting to start a timer that is already running")
            self.eventList.add(t)
        else:
            timer_event = Event(self.time + increment, EventType.TIMERINTERRUPT, entity);
            self.eventList.add(timer_event);


    def stopTimer(self, entity):
        
        if self.trace >= 1:
            print("stopTimer: stopping timer at " + str(self.time))
        timer_event = self.eventList.removeTimer(entity)
        if (timer_event == None):
            if self.trace >= 1:
                print("stopTimer: Warning: Unable to cancel your timer, which is not set.")
                                                    
    def udtSend(self, entity, p):
       
        packet = copy.deepcopy(p)
        
        if packet==None:
            if self.trace >= 1:
                print("udtSend: None" )
        else:    
            if self.trace >= 1:
                print("udtSend: " + packet.toStr())

        if entity == A:
            destination = B
        elif entity == B:
            destination = A 
        else:
            if self.trace >= 1:
                print("entity = " + str(entity))
                print("udtSend: Warning: invalid packet sender")
            return;

        if (random.random() < self.lossProb): 
            if self.trace >= 1:
                print("udtSend: SIMULATING PACKET LOSS")
            return;
    
        if (random.random() < self.corruptProb):
            if self.trace >= 1:
                print("udtSend: SIMULATING PACKET BEING CORRUPTED")

            x = random.random()
            if (x < 0.75):
                payload = packet.payload 
                if len(payload) < 2:
                    payload = "="
                else:
                    payload = "=" + payload[1:]

                packet.payload = payload

            elif (x < 0.875):
                packet.seqNum = random.randint(10, 20)
            else:
                packet.ackNum = random.randint(10, 20)

        arrivalTime = self.eventList.getLastPacketTime(destination)

        if (arrivalTime <= 0.0):
            arrivalTime = self.time

        arrivalTime = arrivalTime + 1.0 + 9.0 * random.random() 

        if self.trace >=2 :
            print("udtSend: Scheduling arrival on other side: at time   " + str(arrivalTime))

        arrival = Event(arrivalTime, EventType.FROMNETWORK, destination, packet);
        self.eventList.add(arrival)
        

    def deliverData(self, entity, dataSent):
        if self.trace >= 1:
            print("B: deliverData: data received at " + str(entity) + ":")


