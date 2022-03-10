#!/usr/bin/python
import sys, os, hashlib
from datetime import datetime

RootDirectory = "/"
IgnoreDirectories = ["/dev", "/proc", "/run", "/sys", "/tmp", "/var/lib", "/var/run"]

def hashFile(filePathName):
    try:
        f = open(filePathName, "rb")
        h = hashlib.sha256()
        h.update(f.read())
        return(h.hexdigest())
    except:
        #print("ERROR: Attempted Hash of "+  str(filePathName) +"\nFailed...")
        return False

def main(): 
    fileDict = {}
    fileList = []
    fileNameList = []
    unHashableList = []
    missingFilesCount= 0
    modifiedFilesCount = 0
    newFilesCount = 0
    movedFilesCount = 0
    delim = ";"
    print("Reading...")
    try:
        readHash = open("hashes.txt", "r")
        unHashable = open("unhashable.txt", "r")
        for filePathUN in unHashable:
            unHashableList.append(filePathUN.strip())
        for line in readHash:
            list = line.split(delim)
            file = list[0]
            fileSplit = file.split("/")
            lenPath = len(fileSplit)
            fileNameList.append(fileSplit[lenPath-1].strip("/"))
            hash = list[1]
            try:
                fileDict[file] = hash
            except:
                print("Could not add to dictionary: " + file)
                continue
        readHash.close()
        unHashable.close()
    except OSError as exception:
        print(exception)
        
    print("Walking...")    
    for root, directories, files in os.walk(RootDirectory, topdown=False):
        for fName in files:
            filePathName = os.path.join(root, fName)
            #print(filePathName)
            if filePathName[0:4] in IgnoreDirectories or filePathName[0:5] in IgnoreDirectories or filePathName[0:8] in IgnoreDirectories:
            	continue
            elif filePathName in unHashableList: #Cannot hash the file in the directory...
            	continue               
            elif fName in fileNameList and filePathName not in fileDict.keys() and fName != "hashes.txt":
                hash = hashFile(filePathName)
                #print(filePathName)
                oldPath = ""
                for key, value in fileDict.items():
                     if hash == value:
                          oldPath = key
                if oldPath == "":
                	continue          
                print("Moved File: " + fName + "\n From: "+ oldPath + " To: "+ filePathName )
                movedFilesCount += 1
                fileList.append(filePathName)
            else:
                fileList.append(filePathName)
            
    writeHash = open("hashes.txt", "w")
    print("Analyzing...")
    for file in fileList:
        curTime = datetime.now()
        timeStamp = curTime.strftime("%d/%m/%Y %H:%M:%S")
        if file in unHashableList:
           print("Not Hashable... Skipping: " + file)	
           continue
        hash = hashFile(file)
        if not hash:
            print("Missing file: " + file)
            missingFilesCount += 1
            continue
        if file not in fileDict.keys():
            print("New file: " + file)
            newFilesCount += 1
            #writeHash.write(file + delim + str(hash) + delim + timeStamp + "\n")
        try:
            if fileDict[file] != hash:
                print("Modified file: " + file)
                modifiedFilesCount += 1
                continue
        except:
            writeHash.write(file + delim + str(hash) + delim + timeStamp + "\n")
        writeHash.write(file + delim + str(hash) + delim + timeStamp + "\n")
    writeHash.close()
    print("\n Summary Report:")    
    print("New files: " + str(newFilesCount))
    print("Missing files: " + str(missingFilesCount))
    print("Modified files " + str(modifiedFilesCount))
    print("Moved files: " + str(movedFilesCount))
    
if __name__=="__main__":
    main()
