#!/usr/bin/python

def parseFromJson(data):
    #print "parseFromJson("+data+")"
    dataDict = {}    
    inKey = False
    inData = False

    #validate curly braces
    if(not(data[0]=='{'and data[-1]=='}')):
        return None
    else:
        inKey = False
        key=""
        dataType = None
        dataStr=""
        inKey=True

        #to handle recursive Json
        depth = 1 
        for char in data[1:]:
            if(char == "{"):
                depth += 1
            if(depth<1):
                return dataDict
            if(char == "}"):
                depth -=1
            if(inKey):
                if(char != ':'):
                    key += char
                else:
                    key = key.strip()
                    inKey = False
            elif not(inKey) and not(inData):
                #the data is a string type
                if (char == "\"" or char == "\'"):
                    dataType = 'str'
                    inData = True 
                elif char.isdigit():
                    dataType = "num"
                    inData = True 
                elif char =="{":
                    dataType = "Json"
                    inData = True
            if inData:
                if (char != ',' and char != '\"' and char != '\'' and char!= '}') or dataType == "Json":
                    dataStr += char
                #seperator character, move onto next key, depth is one if Json has been closed
                if (char == ',' and depth==1) or (char =='}' and depth==0):
                    if dataType == "str":
                        data = dataStr
                    elif dataType =="num":
                        data = float(dataStr)
                    elif dataType == "Json":
                        #must take trailing ',' of dataStr
                        data = parseFromJson(dataStr[:-1])
                    else:
                        return None
                    dataDict[key]=data
                    key = ""
                    dataStr =""
                    inData = False
                    inKey = True

        #Incorrectly formatted string
        if(depth != 0):
            return None
        return dataDict
        print "asdfasdfasdfasdf"

def testJson():
    testCases = ["{command : {device : 'tv', state : 'on'}, command_type : 'relay'}",
                "{command : 'tv', command_type : 'relay', command_meta : 'test'}",
                "{command : 9, command_type : 'relay'}"]
    i =1 
    for testCase in testCases:
        result = parseFromJson(testCase)
        print "Test Case " + str(i)
        print "\tinput: " + testCase
        print "\n\toutput: " + str(result)
        for key in result:
            print "\t" + str(key) + "\t" + str(result[key]) 
        print "\n\n" 
        i+=1
