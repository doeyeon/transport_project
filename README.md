# transport_project

## Overview
Transport layer protocol assignment for Wilfrid Laurier University computer networks course.
This project demonstrates the Alternating-Bit/Stop-And-Wait/rdt.30 protocol for reliable data transfer in the transport layer. It simulates the Application (Sender) -> Transport -> Network <- Transport <- Application (Receiver) network environment.

#### sender.py / receiver.py
These files contain the classes to initialize, send, check, and receive objects of type packet containing objects of type message.

#### network.py
This file is essentially a Mock Object or Stub Routine that acts as a dummied version of the network layer to test the sender and receiver parts of the system.

#### shared.py
This file contains the objects and methods that are shared by the sender and receiver interfaces including the checksum function to ensure all packet data was reliably transported.

#### main.py
This file containts the main interface which prompts the user to set the probabilty of packet loss and corruption in the network simulator.
