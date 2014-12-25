#!/usr/bin/env python
import socket
import time
import thread
import RPi.GPIO as GPIO
import time
import parseFromJson

#needed to setup gpio
GPIO.setmode(GPIO.BOARD)

#keene IR
irIp = "192.168.1.73"
irSource = "192.168.1.250"
irPort = 65432 
irSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
irSock.bind((irSource, irPort))

#process communication
udpIpSource          = "127.0.0.1"  
udpPortSource        = 50008
udpIpDestination     = "127.0.0.1"
udpPortDestination   = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((udpIpSource, udpPortSource))

#load in all the macros
macroFile = open('macros.txt', 'r')
macros = []
for line in macroFile:
        macros.append(line)

#load in all the ir codes
irFile = open('irCodes.txt', 'r')
irCodes = []
for line in irFile:
        irCodes.append(line)

#describes a pin which controls a relay 
class Pin:
        def __init__(self, name, number):
                self.name = name
                self.number = number
                self.locked = False
                self.state = 0
                GPIO.setup(number, GPIO.IN)

        def setState(self, state):
                #only set the pin if it is not locked
                if(not(self.locked)):
                        if(state in [1,"on","ON","On",True,"true","True","1"]):
                                #low impedence, allows relay to turn on 
                                GPIO.setup(self.number, GPIO.OUT)
                                self.state = 1
                        else:
                                #high impedence, does not allow current to flow
                                GPIO.setup(self.number, GPIO.IN)
                                self.state = 0
                else:
                    print "ignored attempt to accessed locked resource " + self.name

#dictionary mapping aliases to pins
pins = {
        "socket6": Pin("socket6",3),
        "ps3": Pin("ps3",5),
        "comp": Pin("comp",8),
        "screenPower": Pin("screenPower",10),
        "sky": Pin("sky",12),
        "sub": Pin("sub",13),
        "tv": Pin("tv",16),
        "socket8": Pin("socket8",18),
        "amp": Pin("amp",19),
        "socket7": Pin("socket7",22),
        "screenDirection": Pin("screenDirection",24),
        "fireplaceSpare": Pin("fireplaceSpare",26)
        }


def irSend(code):
        code = code.strip()
        lineNum=1
        message = False
        index = 0
        while index < len(irCodes) and message == False:
                line = irCodes[index]
                lineSplit = line.split('\t')
                lineSplit[0] = lineSplit[0].strip()
                if lineSplit[0] == code:
                                message = lineSplit[1] 
                index += 1
        print "\t" + str(message)
        if message != False:
                irSock.sendto(message, (irIp, irPort))
        print "\t" + str(code) + ' sent\n'

def findAndExecuteMacro(macroName):
    index = 0
    macroFound = False
    while index < len(macros):
            line = macros[index]
            lineSplit = line.split('\t')
            if lineSplit[0] == macroName:
                    macroLine = line
                    executeMacro(macroLine)
                    macroFound = True
                    break 
            index += 1
    if(not(macroFound)):
            print '\tmacro not found'


def executeMacro(macroLine):
        macroLine = macroLine.strip()
        lineSplit = macroLine.split('\t')
        index = 0
        for i in range(1,len(lineSplit)):
            command = lineSplit[i]
            commandSplit = command.split(',')
            numExecutions = 1
            if i > 0:
                prevCommand = lineSplit[i-1]
                prevCommandSplit = prevCommand.split(',')
                #allows one command to be executed multiple times
                if(prevCommandSplit[0] == 'l' or prevCommandSplit[0] == 'loop'):
                    print "prev command was a loop"
                    numLoops = int(prevCommandSplit[1])
                    if(numLoops > 1):
                        numExecutions = numLoops
                        print numLoops
            if(commandSplit[0] != "loop"):
                printStr =  "\texecuting \"" + command + "\" " 
                if numExecutions > 1:
                    printStr += str(numExecutions) + " times" 
                print printStr
                for i in range(0,numExecutions):
                    executeMacroCommand(command)
            else:
                if(int(commandSplit[1]) != 1):
                    printStr = "\t\"" + command + "\" loop next command "
                    printStr +=  commandSplit[1] + " times"
                    print printStr

#execute a single sub instruction of a macro
def executeMacroCommand(macroCommand):
    elementSplit = macroCommand.split(',')
    if elementSplit[0] == 'r' or elementSplit[0]=='relay':
        #check validity of format
        if(len(elementSplit)==3):
            #look up pin my name
            try:
                targetPin=pins[elementSplit[1]]
                state=elementSplit[2]
                targetPin.setState(elementSplit[2])
            except KeyError:
                print "\t\"" + elementSplit[1] + "\" is not a valid relay name"
        else:
            print "\t\"" + macroCommand + "\"" + "invalid format"
    elif elementSplit[0] == 't':
        if(len(elementSplit)==2):
            try:
                time.sleep(float(elementSplit[1]))                                
            except Exception:
                print "\tcannot convert to float"
        else:
            print "\t\"" + macroCommand + "\"" + "invalid format"
    elif elementSplit[0] == 'ir':
        if(len(elementSplit)==2):
            irSend(str(elementSplit[1]))
            time.sleep(0.25)
        else:
            print "\t\"" + macroCommand + "\"" + "invalid format"
    elif elementSplit[0] == 'lock' or elementSplit[0] == "unlock":
        if(len(elementSplit)==2):
            try:
                targetPin=pins[elementSplit[1]]
                if(elementSplit[0]=="lock"):
                    targetPin.locked = True
                if(elementSplit[0]=="unlock"):
                    targetPin.locked = False 
            except KeyError:
                print "\t\"" + elementSplit[1] + "\" is not a valid relay name"
        else:
            print "\t\"" + macroCommand + "\"" + "invalid format"

def getStatus():
        status = "{"
        for pin in pins:
                status += pins.get(pin).name + " : " +  str(pins.get(pin).state) + ","
        status = status[0:-1]
        status += "}"
        return status

#interperet command
def mainloop(data):
        commandType = data["commandType"]
        if commandType=="ir":
                #return some information about the system (status of pins)
                sock.sendto(getStatus(), (udpIpDestination, udpPortDestination))
                irSend(data["codeName"])
        elif commandType=='macro':
                #return some information about the system (status of pins) before executing lengthly macro
                sock.sendto(getStatus(), (udpIpDestination, udpPortDestination))
                macroName = "" 
                if("macroName" in data):
                    macroName = data["macroName"]
                    print "\tLooking for macro " + macroName
                    findAndExecuteMacro(macroName)
                else:
                    print "\tno macro name given"
        elif commandType=='relay':
                #find the pin you are asked to switch
                device = data["device"]
                targetPin = pins[device]
                #set it to the state you are asked
                state = data["state"]
                targetPin.setState(state)
                #return some information about the system (status of pins)
                sock.sendto(getStatus(), (udpIpDestination, udpPortDestination))


if __name__=="__main__":
    while 1:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        curTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        print curTime + ": data received: " + data
        commandParts = parseFromJson.parseFromJson(data)
        if(commandParts == None):
            print "\timpromperly formatted string"
        else:
            for key in commandParts:
                print "\t" + str(key) + ":\t" + str(commandParts[key]) 
        thread.start_new_thread(mainloop,(commandParts,))

